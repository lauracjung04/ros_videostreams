import glob
import os

import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class VideoPlayerNode(Node):
    def __init__(self):
        super().__init__('video_player_node')

        self.declare_parameter(
            'video_dir', '/home/ljung6/Documents/ros_videostreams/videos'
        )
        self.declare_parameter('video_index', 0)

        video_dir = self.get_parameter('video_dir').value
        index = self.get_parameter('video_index').value

        # Find sample_<index>.* regardless of file extension
        matches = sorted(glob.glob(os.path.join(video_dir, f'sample_{index}.*')))
        if not matches:
            self.get_logger().error(f'No video found for sample_{index} in {video_dir}')
            raise FileNotFoundError(f'sample_{index}.* not found in {video_dir}')

        self.cap = cv2.VideoCapture(matches[0])
        if not self.cap.isOpened():
            raise RuntimeError(f'Could not open {matches[0]}')

        fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.get_logger().info(f'Playing {matches[0]} at {fps:.1f} fps')

        self.pub = self.create_publisher(Image, '/video/image_raw', 10)
        self.create_timer(1.0 / fps, self.publish_frame)

    def publish_frame(self):
        ok, frame = self.cap.read()
        if not ok:
            # End of video: loop back to the start
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        # Build the Image message by hand (avoids needing cv_bridge)
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