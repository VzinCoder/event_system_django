
window.addEventListener('DOMContentLoaded', event => {

    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki
    
    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple, {
            responsive: true,
            language: {
                noRecords: "Nenhum registro encontrado"
            },
            labels: {
                placeholder: "Pesquisar...", // Personalize o placeholder do campo de busca
                perPage: "eventos por página", // Personalize o texto "entries per page"
                noRows: "Nenhum Evento encontrado", // Mensagem quando não há dados
                info: "Mostrando de {start} a {end} de {rows}" // Personalize o texto de informação
            }
        });
    }
});