import glob
import os

import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class VideoPlayerNode(Node):
    def __init__(self):
        super().__init__('video_player_node')

        self.declare_parameter(
            'video_dir', '/home/ljung6/Documents/ros_videostreams/videos'
        )

        self.declare_parameter('video_index', 0)
        self.declare_parameter('video_count', 11)  # sample_0 .. sample_10

        self.video_dir = self.get_parameter('video_dir').value
        self.video_count = self.get_parameter('video_count').value

        self.cap = None
        self.timer = None
        self.index = 0
        self.paused = False

        self.pub = self.create_publisher(Image, '/video/image_raw', 10)
        self.create_subscription(String, '/video_command', self.command_callback, 10)

        initial = self.get_parameter('video_index').value
        if not self.load_video(initial):
            raise RuntimeError(f'Could not load initial video sample_{initial}')

    def load_video(self, index):
        """Open sample_<index>.* and restart playback from the beginning.
        Returns False (and keeps the current video) if it can't be opened."""
        matches = sorted(glob.glob(os.path.join(self.video_dir, f'sample_{index}.*')))
        if not matches:
            self.get_logger().error(f'No video found for sample_{index} in {self.video_dir}')
            return False

        cap = cv2.VideoCapture(matches[0])
        if not cap.isOpened():
            self.get_logger().error(f'Could not open {matches[0]}')
            return False

        # Swap in the new video
        if self.cap is not None:
            self.cap.release()
        self.cap = cap
        self.index = index

        # Restart the timer at this video's frame rate
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        if self.timer is not None:
            self.timer.cancel()
            self.destroy_timer(self.timer)
        self.timer = self.create_timer(1.0 / fps, self.publish_frame)

        self.get_logger().info(f'Playing sample_{index}: {matches[0]} at {fps:.1f} fps')
        return True

    def command_callback(self, msg):
        command = msg.data

        if command == 'play':
            self.paused = False
            self.get_logger().info('Playing')
        elif command == 'pause':
            self.paused = True
            self.get_logger().info('Paused')
        elif command == 'next':
            self.switch_video((self.index + 1) % self.video_count)
        elif command == 'previous':
            self.switch_video((self.index - 1) % self.video_count)
        else:
            self.get_logger().warn(f'Unknown command: {command}')

    def switch_video(self, index):
        if self.load_video(index):
            self.paused = False  # a newly selected video starts playing

    def publish_frame(self):
        if self.paused:
            return  # rqt keeps showing the last frame

        ok, frame = self.cap.read()
        if not ok:
            # End of video: loop back to the start
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        msg = Image()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'video'
        msg.height, msg.width = frame.shape[:2]
        msg.encoding = 'bgr8'
        msg.is_bigendian = 0
        msg.step = msg.width * 3
        msg.data = frame.tobytes()
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = VideoPlayerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()