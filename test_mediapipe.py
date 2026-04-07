import mediapipe as mp

print("MediaPipe 版本:", mp.__version__)

# 新版本的导入方式
print("mp.pose:", mp.pose)
print("mp.solutions.pose 已废弃，使用 mp.pose")