#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import json
import os
import io
from PIL import Image

def load_yolo():
    """Load YOLO model with absolute paths"""
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        weights_path = os.path.join(BASE_DIR, "yolov3.weights")
        config_path = os.path.join(BASE_DIR, "yolov3.cfg")
        names_path = os.path.join(BASE_DIR, "coco.names")

        # Load YOLO
        net = cv2.dnn.readNet(weights_path, config_path)

        # Load class names
        with open(names_path, "r") as f:
            classes = [line.strip() for line in f.readlines()]

        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

        return net, classes, output_layers

    except Exception as e:
        print("YOLO load error:", str(e))
        return None, None, None

def detect_objects(image, net, classes, output_layers):
    """Detect objects in the image"""
    height, width, channels = image.shape
    
    # Detecting objects
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    # Information to show on screen
    class_ids = []
    confidences = []
    boxes = []
    
    # Process each output
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > 0.5:  # Confidence threshold
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    # Apply Non-Maximum Suppression
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    detections = []
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            class_name = classes[class_ids[i]]
            confidence = confidences[i]
            
            detections.append({
                "class": class_name,
                "confidence": round(confidence, 2),
                "bbox": {
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                }
            })
    
    return detections

def main():
    try:
        # Load YOLO model
        net, classes, output_layers = load_yolo()
        
        if net is None:
            result = {
                "error": "Failed to load YOLO model. Check if yolov3.weights, yolov3.cfg, and coco.names exist."
            }
            print(json.dumps(result))
            sys.exit(1)
        
        # Read image from stdin
        image_data = sys.stdin.buffer.read()
        
        if not image_data:
            result = {"error": "No image data received"}
            print(json.dumps(result))
            sys.exit(1)
        
        # Convert bytes to image
        image = Image.open(io.BytesIO(image_data))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detect objects
        detections = detect_objects(image, net, classes, output_layers)
        
        # Return results as JSON
        result = {
            "success": True,
            "detections": detections,
            "count": len(detections)
        }
        
        print(json.dumps(result))
        
    except Exception as e:
        result = {
            "error": f"Detection failed: {str(e)}"
        }
        print(json.dumps(result))
        sys.exit(1)

if __name__ == "__main__":
    main()