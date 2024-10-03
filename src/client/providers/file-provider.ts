import { FILES_URL } from "@/lib/api-endpoints";
import { publicAxios } from "@/lib/axios.config";

export const uploadFile = async (file: Blob) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await publicAxios.post(`${FILES_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('File upload error:', error);
    throw error
  }
};

export const listFiles = async () => {
  try {
    const response = await publicAxios.get(`${FILES_URL}/files`);
    return response.data;
  } catch (error) {
    console.error('File list error:', error);
    throw error;
  }
};

export const deleteFile = async (fileName: string) => {
  try {
    const response = await publicAxios.delete(`${FILES_URL}/delete`, {
      params: { file_name: fileName },
    });
    return response.data;
  } catch (error) {
    console.error('File delete error:', error);
    throw error;
  }
};