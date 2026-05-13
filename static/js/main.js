document.addEventListener('DOMContentLoaded', function() {
    // Toggle Sidebar no Mobile
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.querySelector('#wrapper').classList.toggle('toggled');
        });
    }

    // Fechar sidebar ao clicar fora (no mobile)
    document.addEventListener('click', function(e) {
        const wrapper = document.getElementById('wrapper');
        const sidebar = document.getElementById('sidebar-wrapper');
        const toggleBtn = document.getElementById('sidebarToggle');
        
        if (wrapper.classList.contains('toggled')) {
            if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                wrapper.classList.remove('toggled');
            }
        }
    });

    // Fechar alertas automaticamente após 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
