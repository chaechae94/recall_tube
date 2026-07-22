from scenedetect import SceneManager, open_video
from scenedetect.detectors import ContentDetector


def detect_scenes(file_path: str) -> list[dict]:
    video = open_video(file_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    scene_manager.detect_scenes(video)
    scene_list = scene_manager.get_scene_list()

    if not scene_list:
        duration = video.duration.get_seconds()
        return [{"start": 0.0, "end": duration}]

    return [
        {"start": start.get_seconds(), "end": end.get_seconds()}
        for start, end in scene_list
    ]
