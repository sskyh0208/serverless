import axios from "axios";
import { API_URL } from "@/lib/api-endpoints";

// クレデンシャルを含まないリクエスト用（ログイン前など）
const publicAxios = axios.create({
  baseURL: API_URL,
  headers: {
    Accept: "application/json",
  },
});

// クレデンシャルを含むリクエスト用（ログイン後など）
const privateAxios = axios.create({
  baseURL: API_URL,
  headers: {
    Accept: "application/json",
  },
  withCredentials: true,
});

export { publicAxios, privateAxios };