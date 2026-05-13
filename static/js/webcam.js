document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('videoElement');
    const canvasOverlay = document.getElementById('canvasOverlay');
    const btnStart = document.getElementById('btnStart');
    const btnStop = document.getElementById('btnStop');
    const loadingCam = document.getElementById('loadingCam');
    
    const resNome = document.getElementById('resNome');
    const resConfianca = document.getElementById('resConfianca');
    const resultContainer = document.getElementById('resultContainer');
    
    let stream = null;
    let processingInterval = null;
    let isProcessing = false;

    // Ajusta o canvas overlay para o tamanho do video
    function resizeCanvas() {
        if(video.videoWidth) {
            canvasOverlay.width = video.clientWidth;
            canvasOverlay.height = video.clientHeight;
        }
    }

    window.addEventListener('resize', resizeCanvas);

    async function startCamera() {
        try {
            loadingCam.style.display = 'block';
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 640, height: 480, facingMode: 'user' } 
            });
            video.srcObject = stream;
            video.style.display = 'block';
            
            video.onloadedmetadata = () => {
                loadingCam.style.display = 'none';
                resizeCanvas();
                btnStart.disabled = true;
                btnStop.disabled = false;
                
                // Iniciar loop de processamento a cada 1 segundo (evita sobrecarga no backend)
                processingInterval = setInterval(processFrame, 1000);
            };
        } catch (err) {
            console.error("Erro ao acessar webcam:", err);
            loadingCam.innerHTML = `<p class="text-danger"><i class="bi bi-exclamation-triangle"></i> Erro ao acessar câmera: ${err.message}</p>`;
        }
    }

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            video.srcObject = null;
            video.style.display = 'none';
            loadingCam.style.display = 'block';
            loadingCam.innerHTML = '<p>Câmera parada.</p>';
            
            clearInterval(processingInterval);
            
            btnStart.disabled = false;
            btnStop.disabled = true;
            
            resNome.textContent = 'Aguardando...';
            resConfianca.textContent = '--';
            resultContainer.classList.remove('bg-success', 'bg-opacity-10', 'border-success');
        }
    }

    async function processFrame() {
        if (isProcessing || !stream) return;
        isProcessing = true;

        // Desenhar frame atual num canvas em memória para pegar base64
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Pegar qualidade baixa para ser rápido
        const base64Image = canvas.toDataURL('image/jpeg', 0.7);

        try {
            const response = await fetch('/api/reconhecer/frame', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: base64Image })
            });

            const data = await response.json();
            
            if (data.success) {
                resNome.textContent = data.nome;
                resNome.classList.remove('text-muted');
                resNome.classList.add('text-success', 'fw-bold');
                
                resConfianca.textContent = `Confiança: ${data.confianca}%`;
                resultContainer.classList.add('bg-success', 'bg-opacity-10', 'border', 'border-success', 'rounded');
            } else {
                resNome.textContent = 'Não identificado';
                resNome.classList.remove('text-success', 'fw-bold');
                resNome.classList.add('text-muted');
                
                resConfianca.textContent = '--';
                resultContainer.classList.remove('bg-success', 'bg-opacity-10', 'border-success');
            }
        } catch (error) {
            console.error("Erro ao enviar frame:", error);
        } finally {
            isProcessing = false;
        }
    }

    btnStart.addEventListener('click', startCamera);
    btnStop.addEventListener('click', stopCamera);
});
