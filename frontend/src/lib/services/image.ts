interface UploadResponse {
  success: boolean;
  data?: {
    url: string;
    delete_url?: string; // 添加 delete_url
    thumb:{
      url: string;
    }
  };
  error?: {
    message: string;
  };
}

interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

type ProgressCallback = (progress: UploadProgress) => void;

export async function uploadToImgBB(
  file: File,
  onProgress?: ProgressCallback
): Promise<UploadResponse> {
  const API_KEY = 'dc1398dd7ba5dc154d50c82c42bf18c6';
  const formData = new FormData();
  formData.append('image', file);

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.open('POST', `https://api.imgbb.com/1/upload?key=${API_KEY}`, true);

    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable && onProgress) {
        const progress: UploadProgress = {
          loaded: event.loaded,
          total: event.total,
          percentage: Math.round((event.loaded / event.total) * 100)
        };
        onProgress(progress);
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const result = JSON.parse(xhr.responseText);
          resolve(result);
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (e) {
          reject(new Error('Failed to parse response'));
        }
      } else {
        reject(new Error(`HTTP error: ${xhr.status} ${xhr.statusText}`));
      }
    });

    xhr.addEventListener('error', () => {
      reject(new Error('Network error'));
    });

    xhr.send(formData);
  });
}