from hacadet_pkg import *
import multiprocessing as mp


def main(n):
    # Initialize components
    bmw_model = YOLO(BMW_MODEL_PATH)
    sound = SoundManager()
    capture = get_capture(n)
    frame_count = 0
    paused = False
    terminated = False

    while not terminated:
        if not paused:
            while capture.isOpened():
                success, frame = capture.read()
                # print(frame.shape)
                if not success:
                    print("Reconnecting...")
                    capture = get_capture(n)
                    continue
                width = frame.shape[1]
                # frame = resize_frame(frame)

                if frame_count % FRAME_SKIP == 0:
                    # Process frame
                    cables, skids, frame = detect_objects(frame, bmw_model)
                    alert = check_alert(cables, skids, THRESHOLD, width)
                    cv.namedWindow(f"HaCaDet - Camera {n}", cv.WINDOW_NORMAL)
                    # cv.setWindowProperty(f"HaCaDet - Camera {n}", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
                    cv.imshow(f"HaCaDet - Camera {n}", frame)
                    # Handle alerts
                    if alert:
                        save_frame(frame, frame_count)
                        print(f"{alert.capitalize()} Alert!!!")
                        sound.play(alert)
                        print("Press 'p' to mute")
                        while True:
                            cv.setWindowProperty(f"HaCaDet - Camera {n}", cv.WND_PROP_TOPMOST, 3)
                            cv.imshow(f"HaCaDet - Camera {n}", frame)
                            key = cv.waitKey(5000)
                            if key == ord('p'):
                                sound.stop(alert)
                                cv.namedWindow("HaCaDet-Fix the issue!!!", cv.WINDOW_NORMAL)
                                cv.setWindowProperty("HaCaDet-Fix the issue!!!", cv.WND_PROP_TOPMOST, 1)
                                cv.imshow("HaCaDet-Fix the issue!!!", frame)
                                print("Fix the issue; press 'p' to resume; 'Esc' to terminate")
                                key = cv.waitKey(0)
                                if key == 27:
                                    terminated = True
                                    break
                                elif key == ord('p'):
                                    cv.destroyWindow("HaCaDet-Fix the issue!!!")
                                    break
                            else:
                                sound.stop(alert)
                                print("Time Out")
                                break
                        if terminated:
                            break
                    else:
                        # Check for normal operation keys
                        key = cv.waitKey(20)
                        if key == ord('p'):
                            paused = True
                            break
                        elif key == 27:
                            terminated = True
                            break

                frame_count += 1

            # Paused state handling
            if paused and not terminated:
                print("PAUSED - Press 'p' to continue or 'Esc' to terminate")
                while True:
                    key = cv.waitKey(0)
                    if key == ord('p'):
                        paused = False
                        break
                    elif key == 27:
                        terminated = True
                        break

    # Cleanup
    capture.release()
    cv.destroyAllWindows()
    print("HaCaDet terminated successfully")


if __name__ == "__main__":
    print("\nProject HaCaDet: No more low hanging cables!!!")
    for i in range(len(CAMERA_URL)):
        mp.Process(target=main, args=[i]).start()

    children = mp.active_children()

    for child in children:
        child.join()
