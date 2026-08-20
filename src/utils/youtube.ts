/**
 * Extract YouTube video ID from various URL formats
 * Examples:
 * - https://www.youtube.com/watch?v=dQw4w9WgXcQ -> dQw4w9WgXcQ
 * - https://youtu.be/dQw4w9WgXcQ -> dQw4w9WgXcQ
 * - https://www.youtube.com/embed/dQw4w9WgXcQ -> dQw4w9WgXcQ
 */
export function extractYouTubeId(url: string): string {
  const patterns = [
    /(?:youtube\.com\/watch\?v=)([^&]+)/,
    /(?:youtu\.be\/)([^?]+)/,
    /(?:youtube\.com\/embed\/)([^?]+)/,
  ];

  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) {
      return match[1];
    }
  }

  // If no pattern matches, return the original URL (might already be just the ID)
  return url;
}
