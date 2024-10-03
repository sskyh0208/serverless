"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Upload, Trash2 } from "lucide-react";
import { uploadFile, listFiles, deleteFile } from "@/providers/file-provider";
import { toast } from 'sonner';
import { LoadingIcon } from '@/components/LoadingIcon';
import ConfirmationModal from '@/components/ConfirmationModal';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface FileInfo {
  key: string;
  size: number;
  last_modified: string;
}

export default function FilesPage() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [fileToDelete, setFileToDelete] = useState<string | null>(null);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    setIsLoading(true);
    try {
      const result = await listFiles();
      setFiles(Array.isArray(result.files) ? result.files : []);
    } catch (error: any) {
      toast.error(`ファイル一覧の取得に失敗しました`);
      setFiles([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (file) {
      setIsUploading(true);
      try {
        const result: any = await uploadFile(file);
        console.log(result);
        toast.success(`ファイルがアップロードされました: ${result.key}`);
        fetchFiles(); // ファイル一覧を更新
      } catch (error: any) {
        toast.error(`ファイルのアップロードに失敗しました`);
      } finally {
        setIsUploading(false);
        setFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      }
    }
  };

  const handleDeleteClick = (fileName: string) => {
    setFileToDelete(fileName);
    setIsDeleteModalOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (fileToDelete) {
      try {
        await deleteFile(fileToDelete);
        toast.success(`ファイルが削除されました: ${fileToDelete}`);
        fetchFiles(); // ファイル一覧を更新
      } catch (error: any) {
        toast.error(`ファイルの削除に失敗しました: ${error.message}`);
      } finally {
        setIsDeleteModalOpen(false);
        setFileToDelete(null);
      }
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="h-full max-w-[912px] px-3 mx-auto">
      <h1 className="text-2xl font-bold text-neutral-700 mb-6">
        ファイルページ
      </h1>
      <div className="flex items-center space-x-4 mb-8">
        <div className="flex-grow">
          <Input 
            id="file-upload" 
            type="file" 
            onChange={handleFileChange}
            className="h-10"
            ref={fileInputRef}
          />
        </div>
        <Button
          onClick={handleUpload}
          disabled={!file || isUploading}
          className="h-10 whitespace-nowrap"
        >
          {isUploading ? (
            <>
              <LoadingIcon height={24} width={24} /> アップロード中...
            </>
          ) : (
            <>
              <Upload className="mr-2 h-4 w-4" /> アップロード
            </>
          )}
        </Button>
      </div>

      <h2 className="text-xl font-semibold text-neutral-700 mb-4">ファイル一覧</h2>
      {isLoading ? (
        <div className="flex justify-center items-center h-[400px]">
          <LoadingIcon /> 読み込み中...
        </div>
      ) : (
        <div className="relative overflow-hidden border rounded-md" style={{ height: '400px' }}>
          <Table>
            <TableHeader className="sticky top-0 bg-white z-10">
              <TableRow>
                <TableHead className="w-[40%]">ファイル名</TableHead>
                <TableHead className="w-[20%] text-left">サイズ</TableHead>
                <TableHead className="w-[30%] text-left">最終更新日</TableHead>
                <TableHead className="w-[10%]"></TableHead>
              </TableRow>
            </TableHeader>
          </Table>
          <div className="overflow-auto" style={{ height: 'calc(400px - 2.5rem)' }}>
            <Table>
              <TableBody>
                {files.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center">ファイルがありません。</TableCell>
                  </TableRow>
                ) : (
                  files.map((file, index) => (
                    <TableRow key={index}>
                      <TableCell className="w-[40%] font-medium">{file.key}</TableCell>
                      <TableCell className="w-[20%] text-left">{formatFileSize(file.size)}</TableCell>
                      <TableCell className="w-[30%] text-left">{file.last_modified}</TableCell>
                      <TableCell className="w-[10%]">
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleDeleteClick(file.key)}
                          className="w-full"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </div>
      )}

      <ConfirmationModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onConfirm={handleDeleteConfirm}
        title="ファイル削除の確認"
        message={`"${fileToDelete}" を削除してもよろしいですか？`}
        confirmText="削除"
        cancelText="キャンセル"
      />
    </div>
  );
}