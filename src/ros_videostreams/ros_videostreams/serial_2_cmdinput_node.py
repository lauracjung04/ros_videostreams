import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, Bool, String

POT_MIN = 0
POT_MAX = 1023

class serial_2_cmdinput_node(Node):
    def __init__(self):
        super().__init__('serial_2_cmdinput_node')

        self.last_pot = None      # last pot value seen
        self.last_button = False  # last button state seen

        self.pot_sub = self.create_subscription(
            Int32, '/potentiometer', self.pot_callback, 10)
        self.button_sub = self.create_subscription(
            Bool, '/button', self.button_callback, 10)

        self.cmd_pub = self.create_publisher(String, '/video_command', 10)


    def send_command(self, cmd: str):
        msg = String()
        msg.data = cmd
        self.cmd_pub.publish(msg)
        self.get_logger().info(f'Sent: {cmd}')

    def pot_callback(self, msg: Int32):
        value = msg.data

        # Only act when the value CHANGES to max or min
        if self.last_pot is not None and value != self.last_pot:
            if value == POT_MAX:
                self.send_command('next')
            elif value == POT_MIN:
                self.send_command('previous')

        self.last_pot = value

    def button_callback(self, msg: Bool):
        # Rising edge only: false -> true counts as one press
        if msg.data and not self.last_button:
            self.send_command('play/pause')

        self.last_button = msg.data


def main(args=None):
    rclpy.init(args=args)
    node = serial_2_cmdinput_node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()