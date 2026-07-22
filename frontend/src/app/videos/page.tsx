"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { ApiError, VideoRead, getMyVideos } from "@/lib/api";

export default function VideosPage() {
  const router = useRouter();
  const [videos, setVideos] = useState<VideoRead[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
      return;
    }

    getMyVideos(token)
      .then(setVideos)
      .catch((err) => {
        if (err instanceof ApiError && err.status === 401) {
          localStorage.removeItem("access_token");
          router.push("/login");
          return;
        }
        setError(err instanceof ApiError ? err.message : "영상 목록을 불러오지 못했습니다.");
      });
  }, [router]);

  return (
    <main style={{ maxWidth: 480, margin: "80px auto", fontFamily: "sans-serif" }}>
      <h1>내 영상</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {!error && videos === null && <p>불러오는 중...</p>}
      {videos !== null && videos.length === 0 && <p>업로드한 영상이 없습니다.</p>}
      {videos !== null && videos.length > 0 && (
        <ul>
          {videos.map((video) => (
            <li key={video.id}>{video.title}</li>
          ))}
        </ul>
      )}
    </main>
  );
}
