import pyrealsense2 as rs
import numpy as np
import cv2
from datetime import datetime, timedelta
import time


def list_realsense_cameras():
    ret = []
    # RealSense 컨텍스트 생성
    context = rs.context()
    # 연결된 모든 장치를 가져옴
    devices = context.query_devices()
    
    # 장치가 없을 경우 출력
    if len(devices) == 0:
        print("No RealSense devices connected.")
        return
    
    # 각 장치의 시리얼 번호 출력
    for device in devices:
        serial_number = device.get_info(rs.camera_info.serial_number)
        ret.append(serial_number)
        print(f"Device with serial number: {serial_number}")

    print(ret)
    return  ret
    
    
def save_frames(frames, frame_number, orig=False):
    for serial, frame in frames.items():
        color_frame = frame.get_color_frame()

        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        
        current_tick = time.time()
        elapsed = current_tick - start_tick
        current_time = str(start_time + timedelta(seconds=elapsed))[:-7]
        
        timestamp = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        color_filename = f"/home/bean/Pictures/0_rgb_{serial}_{timestamp}_{frame_number}.png"

        if orig == True:
            color_filename = f"/home/bean/Pictures/rgb_{serial}_{timestamp}_{frame_number}.png"
            
        cv2.imwrite(color_filename, color_image)

        

        
        
def main(x1, y1, orig=False):
    # 카메라 파이프라인과 설정 초기화
    pipelines = {}
    config = rs.config()

    for serial in serial_numbers:
        pipeline = rs.pipeline()
        config.enable_device(serial)
        config.enable_stream(rs.stream.color, x1, y1, rs.format.bgr8, 30)
        pipeline.start(config)
        pipelines[serial] = pipeline


    try:
        frame_number = 0
        while True:
            frames = {}
            for serial, pipeline in pipelines.items():
                frames[serial] = pipeline.wait_for_frames()
            if orig == False:
                save_frames(frames, frame_number)
            else:
                save_frames(frames, frame_number, orig=True)
            frame_number += 1

            if frame_number >= 1:  # 원하는 프레임 수를 설정
                break
            

    finally:
        for pipeline in pipelines.values():
            pipeline.stop()
            
            

if __name__ == "__main__":
    serial_numbers = list_realsense_cameras()
    
    # program starting time
    start_time = datetime(2024, 7, 16, 12, 0, 0)
    start_tick = time.time()
    
    while True:
	    # main(640, 480)
        main(1280, 720, orig=True)
        time.sleep(5)
