import cv2
import math

p1 = 530
p2 = 300

xs = []
ys = []

video = cv2.VideoCapture("footvolleyball.mp4")

# Load tracker (Switched to KCF for better performance with smaller boxes)
tracker = cv2.TrackerKCF_create()

# Read the first frame of the video
success, img = video.read()

# Select the bounding box on the image
bbox = cv2.selectROI("tracking", img, False)

# Initialize the tracker with the first frame and the bounding box
tracker.init(img, bbox)

def goal_track(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    c1 = x + int(w/2)
    c2 = y + int(h/2)
    cv2.circle(img, (c1, c2), 2, (0, 0, 255), 5)

    cv2.circle(img, (int(p1), int(p2)), 2, (0, 255, 0), 3)
    dist = math.sqrt(((c1-p1)**2) + (c2-p2)**2)
    print(dist)

    if dist <= 20:
        cv2.putText(img, "Goal", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    xs.append(c1)
    ys.append(c2)

    for i in range(len(xs)-1):
        cv2.circle(img, (xs[i], ys[i]), 2, (0, 0, 255), 5)

while True:
    # Read the video and store the values in 'check' and 'img' variables
    success, img = video.read()

    # Check if we are getting the updated image to draw the tracking box
    if success:
        # Update the tracker
        success, bbox = tracker.update(img)

        # If tracking is successful, draw the bounding box
        if success:
            # Check if the bounding box is too small or too large
            if bbox[2] < 10 or bbox[3] < 10:
                # Reinitialize the tracker if the box is too small
                tracker.clear()
                tracker = cv2.TrackerKCF_create()
                tracker.init(img, bbox)
            else:
                goal_track(img, bbox)  # Call goal_track function
                x, y, w, h = [int(i) for i in bbox]
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
                cv2.putText(img, "Tracking", (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(img, "LOST", (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the frame
        cv2.imshow("Tracking", img)

        # Press 'Q' key to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

video.release()
cv2.destroyAllWindows()
