declare module 'jspdf' {
  export default class jsPDF {
    constructor();
    setFontSize(size: number): void;
    text(text: string, x: number, y: number): void;
    splitTextToSize(text: string, maxWidth: number): string[];
    output(type: string): Blob;
  }
} 