import cv2
import numpy as np
from sklearn.cluster import KMeans
from skimage import color
from skimage.filters import gaussian
from scipy import ndimage

def segment_burgers_advanced(frame, n_clusters=3, sigma=1):
    # Convert the image from BGR to RGB
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Apply Gaussian blur to reduce noise
    blurred = gaussian(rgb_image, sigma=sigma, channel_axis=-1)

    # Reshape the image to a 2D array of pixels
    pixel_values = blurred.reshape((-1, 3))

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(pixel_values)

    # Reshape the labels back to the image shape
    segmented = kmeans.labels_.reshape(rgb_image.shape[:2])

    # Identify the cluster that likely represents the burgers (usually the middle intensity)
    cluster_centers = kmeans.cluster_centers_
    burger_cluster = np.argsort(np.mean(cluster_centers, axis=1))[1]

    # Create a binary mask for the burger cluster
    burger_mask = (segmented == burger_cluster).astype(np.uint8) * 255

    # Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    burger_mask = cv2.morphologyEx(burger_mask, cv2.MORPH_CLOSE, kernel)
    burger_mask = cv2.morphologyEx(burger_mask, cv2.MORPH_OPEN, kernel)

    return burger_mask


def remove_small_objects(image, size_threshold):

    # Find contours
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask to draw small objects
    mask = np.zeros(image.shape, dtype=np.uint8)

    # Filter and draw contours smaller than the threshold
    for contour in contours:
        if cv2.contourArea(contour) > size_threshold:
            cv2.drawContours(mask, [contour], 0, (255), -1)

    # Apply the mask to the original image
    result = cv2.bitwise_and(image, mask)

    return result


def fill_gaps(image, size_threshold):
    # Invert the image
    image_inverted = cv2.bitwise_not(image)

    # Label connected components
    labeled, num_features = ndimage.label(image_inverted)

    # Find the label of the largest component (background)
    sizes = np.bincount(labeled.ravel())
    largest_label = sizes[1:].argmax() + 1  # +1 because background is labeled 0

    # Create a mask of the largest component
    background_mask = (labeled == largest_label)

    # Convert back to uint8
    result = background_mask.astype(np.uint8) * 255

    return result

    return result