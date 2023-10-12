const video = document.getElementById('camera');
        const canvas = document.getElementById('snapshot');
        const cameraImage = document.getElementById('camera_image');
        const startCameraBtn = document.getElementById('startCameraBtn');
        const captureBtn = document.getElementById('captureBtn');
        const preview = document.getElementById('preview');
        const previewImg = document.getElementById('previewImg');
        const form = document.getElementById('input');

        let stream;

        // When user clicks "Open Camera"
        startCameraBtn.onclick = async () => {
            try {
                // Request camera access
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { 
                        width: { ideal: 320 },
                        height: { ideal: 240 },
                        facingMode: 'user' // Use front camera on mobile
                    } 
                });
                
                video.srcObject = stream;
                video.style.display = 'block';
                captureBtn.style.display = 'inline-block';
                startCameraBtn.style.display = 'none';
                
                // Wait for video to load and set canvas dimensions
                video.onloadedmetadata = () => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                };
                
            } catch (err) {
                alert("Could not access the camera. Please make sure you've granted camera permissions.");
                console.error('Camera access error:', err);
            }
        };

        captureBtn.onclick = () => {
        if (video.videoWidth === 0 || video.videoHeight === 0) {
            alert("Please wait for the camera to fully load before capturing.");
            return;
        }

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const context = canvas.getContext('2d');
        context.save(); // Save current context state

        // Flip horizontally
        context.translate(canvas.width, 0);
        context.scale(-1, 1);

        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        context.restore(); // Restore context to original state

        const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
        cameraImage.value = dataUrl;

        previewImg.src = dataUrl;
        preview.style.display = 'block';

        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }

        video.style.display = 'none';
        captureBtn.style.display = 'none';
        startCameraBtn.style.display = 'inline-block';
    };


        // Handle form submission
        form.onsubmit = (e) => {            
            const formData = new FormData(form);
            
            // Check what data we have
            const fileInput = document.getElementById('myFile');
            const cameraData = cameraImage.value;
            
            if (fileInput.files.length > 0) {
                console.log('File selected:', fileInput.files[0].name);
            } else if (cameraData) {
                console.log('Camera image captured');
                // Convert base64 to blob for proper file upload
                const base64Data = cameraData.split(',')[1];
                const byteCharacters = atob(base64Data);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);
                const blob = new Blob([byteArray], { type: 'image/jpeg' });
                
                // Add the blob as a file to the form data
                formData.append('camera_file', blob, 'camera_capture.jpg');
            } else {
                alert('Please select a file or capture a photo first.');
                return;
            }
            
            
            form.submit();
        };