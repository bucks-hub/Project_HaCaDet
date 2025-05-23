from hacadet import *


def main():
    # Initialize components
    bmw_model = YOLO(BMW_MODEL_PATH)
    sound = SoundManager()
    capture = get_capture()
    frame_count = 0
    paused = False
    terminated = False

    while not terminated:
        if not paused:
            while capture.isOpened():
                success, frame = capture.read()
                if not success:
                    print("Reconnecting...")
                    capture = get_capture()
                    continue

                frame = resize_frame(frame)

                if frame_count % FRAME_SKIP == 0:
                    # Process frame
                    cables, skids, frame = detect_objects(frame, bmw_model)
                    alert = check_alert(cables, skids, THRESHOLD)

                    # Handle alerts
                    if alert:
                        save_frame(frame, frame_count)
                        print(f"{alert.capitalize()} Alert!!!")
                        sound.play(alert)
                        print("Press 's' to stop alarm")
                        while True:
                            key = cv.waitKey(0)
                            if key == ord('s'):
                                sound.stop(alert)
                                break

                    cv.imshow("output", frame)

                # Check for normal operation keys
                key = cv.waitKey(20)
                if key == ord('p'):
                    paused = True
                    break
                elif key == ord('t'):
                    terminated = True
                    break

                frame_count += 1

        # Paused state handling
        if paused and not terminated:
            print("PAUSED - Press 'c' to continue or 't' to terminate")
            while True:
                key = cv.waitKey(0)
                if key == ord('c'):
                    paused = False
                    break
                elif key == ord('t'):
                    terminated = True
                    break

    # Cleanup
    capture.release()
    cv.destroyAllWindows()
    print("HaCaDet terminated successfully")


if __name__ == "__main__":
    main()
