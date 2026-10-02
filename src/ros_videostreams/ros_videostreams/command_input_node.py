import threading

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# What the user can type -> what gets published
COMMANDS = {
    'next': 'next',
    'previous': 'previous',
    'play': 'play',
    'pause': 'pause',
}


class CommandInputNode(Node):
    def __init__(self):
        super().__init__('command_input_node')
        self.pub = self.create_publisher(String, '/video_command', 10)

        # input() blocks, so run it in a background thread
        threading.Thread(target=self.input_loop, daemon=True).start()

    def input_loop(self):
        print('Commands: next, previous, play,pause (Ctrl+C to quit)')
        while rclpy.ok():
            try:
                text = input('> ').strip().lower()
            except EOFError:
                break

            if not text:
                continue

            command = COMMANDS.get(text)
            if command is None:
                print(f'Unknown command "{text}". Use: next, previous, play, pause')
                continue

            self.pub.publish(String(data=command))
            print(f'Sent: {command}')


def main(args=None):
    rclpy.init(args=args)
    node = CommandInputNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()