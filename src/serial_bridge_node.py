import re
import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import Bool, Int32

#collected message from serial
LINE_RE=re.compile(
     r"Analog:\s*(\d+),\s*Voltage:\s*([\d.]+),\s*Button Pressed:\s*([01])"
)

class serial_bridge_node(Node):
    def __init__(self):
        super().__init__('serial_bridge_node')
 
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 115200)  # must match the Arduino sketch
 
        port = self.get_parameter('port').value
        baud = self.get_parameter('baud_rate').value
 
        self.pot_pub = self.create_publisher(Int32, '/potentiometer', 10)
        self.button_pub = self.create_publisher(Bool, '/button', 10)
 
        self.buffer = b''
        self.ser = serial.Serial(port, baud, timeout=0)  # non-blocking
        self.get_logger().info(f'Opened {port} @ {baud} baud')
 
        # Poll the serial port at 100 Hz
        self.create_timer(0.01, self.read_serial)

    def read_serial(self):
        try:
            waiting = self.ser.in_waiting
            if waiting:
                self.buffer += self.ser.read(waiting)
        except serial.SerialException as e:
            self.get_logger().error(f'Serial error: {e}')
            return

        # Split into complete lines; keep any partial line for next time
        *lines, self.buffer = self.buffer.split(b'\n')
        for raw in lines:
            self.handle_line(raw.decode('utf-8', errors='ignore').strip())

    def handle_line(self, line):
        match = LINE_RE.search(line)
        if not match:
            return  # skip malformed lines (common at startup)

        analog = int(match.group(1))
        pressed = match.group(3) == '1'

        self.pot_pub.publish(Int32(data=analog))
        self.button_pub.publish(Bool(data=pressed))

def main(args=None):
    rclpy.init(args=args)
    node = serial_bridge_node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
    