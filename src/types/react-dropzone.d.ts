declare module 'react-dropzone' {
  import { ComponentType } from 'react';

  interface DropzoneOptions {
    onDrop?: (acceptedFiles: File[], rejectedFiles: any[], event: any) => void;
    accept?: Record<string, string[]>;
    multiple?: boolean;
    disabled?: boolean;
  }

  interface DropzoneState {
    isDragActive: boolean;
    isDragAccept: boolean;
    isDragReject: boolean;
  }

  interface DropzoneRef {
    open: () => void;
  }

  interface UseDropzoneReturn {
    getRootProps: (props?: any) => any;
    getInputProps: (props?: any) => any;
    open: () => void;
    isDragActive: boolean;
    isDragAccept: boolean;
    isDragReject: boolean;
  }

  export function useDropzone(options?: DropzoneOptions): UseDropzoneReturn;
} 