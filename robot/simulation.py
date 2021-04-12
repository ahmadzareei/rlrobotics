from models.robot import Robot
import numpy as np
from pathlib import Path
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
from utils import Utils
import time


class Simulation:
    def __init__(self):
        self.robot = Robot()

        steps = 50
        # Initialize the videos
        self.blocks_video = self.init_video('{0}/blocks/out.mp4'.format(Path(__file__).resolve().parent))

        self.actuation1_direction = np.concatenate(
            (np.zeros(steps), np.ones(steps)),
            axis=0
        ) < 1

        self.actuation2_direction = np.concatenate(
            (np.zeros(steps), np.ones(steps)),
            axis=0
        ) > 0

        self.actuation1 = np.concatenate(
            (
                np.linspace(0, 0.044721 * 2, num=steps),
                np.linspace(0.044721 * 2, 0, num=steps)
            ),
            axis=0
        )

        self.actuation2 = np.concatenate(
            (
                np.linspace(0, -0.044721 * 2, num=steps),
                np.linspace(-0.044721 * 2, 0, num=steps)
            ),
            axis=0
        )

        self.actuation1 = np.tile(self.actuation1, 2)
        self.actuation2 = np.tile(self.actuation2, 2)
        self.actuation1_direction = np.tile(self.actuation1_direction, 2)
        self.actuation2_direction = np.tile(self.actuation2_direction, 2)
        self.steps = steps

    def simulate(self):
        start_time = time.time()
        for a_1, a_2, d_1, d_2, s in zip(self.actuation1,
                                         self.actuation2,
                                         self.actuation1_direction,
                                         self.actuation2_direction,
                                         range(len(self.actuation1))):

            print('step : {}'.format(s))
            self.robot.update_position(a_1, a_2, d_1, d_2)
            self.draw_blocks()

        end_time = time.time()

        print("Simulation time : {0}s".format(end_time - start_time))

        self.save_video(self.blocks_video)

    def draw_blocks(self):
        # Draw blocks
        self.new_frame()
        self.robot.draw(self.frame)
        self.blocks_video.write(self.frame)

    def init_video(self, name):
        fourcc = VideoWriter_fourcc('m', 'p', '4', 'v')
        self.create_main_frame()
        return VideoWriter(name, fourcc, float(Utils.FPS), (Utils.WIDTH, Utils.HEIGHT))

    def create_main_frame(self):
        frame = np.ones((Utils.HEIGHT, Utils.WIDTH, 3), dtype=np.uint8) * 255
        # Get the visual plane coordinates
        max_coordinates = Utils.Pixel2Coordinate(Utils.WIDTH, Utils.HEIGHT)
        max_x = max_coordinates.x
        max_y = max_coordinates.y

        # Draw middle cross lines
        cv2.line(
            frame,
            (
                Utils.ConvertX(0),
                Utils.ConvertY(-max_y)
            ),
            (
                Utils.ConvertX(0),
                Utils.ConvertY(max_y)
            ),
            color=Utils.light_gray,
            thickness=1
        )

        cv2.line(
            frame,
            (
                Utils.ConvertX(-max_x),
                Utils.ConvertY(0)
            ),
            (
                Utils.ConvertX(max_x),
                Utils.ConvertY(0)
            ),
            color=Utils.light_gray,
            thickness=1
        )
        self.main_frame = frame

    def new_frame(self):
        self.frame = self.main_frame.copy()

    def save_video(self, video):
        video.release()
