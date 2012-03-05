$(document).ready(function(){
  //Especificamos los dos procesos de cierre y apertura del men� secundario
  $('#menu-secundario a').click(function() {
    mychildren = $(this).next('ul');
    if ( mychildren.length > 0 ){
      myarrow = $(this).find('img');
      mychildren.animate({height: 'toggle'}, 300,function(){
        recalcula_alturas();
      });
      mysrc = myarrow.attr('src');
      if (mysrc.search('cerrado_p') != -1 ) {
        myarrow.replaceWith( '<img src="/media/img/ico_abierto_p.png" width="12" height="7" alt="men� abierto" />' );
        //myarrow.replaceWith( '<img src="i/ico_abierto_p.png" width="12" height="7" alt="men� abierto" />' );
        return false;
      } else if (mysrc.search('abierto_p') != -1 ) {
        myarrow.replaceWith( '<img src="/media/img/ico_cerrado_p.png" width="7" height="12" alt="men� cerrado" />' );
        //myarrow.replaceWith( '<img src="imagenes/ico_cerrado_p.png" width="7" height="12" alt="men� cerrado" />' );
        return false;
      } else if (mysrc.search('cerrado') != -1 ) {
        myarrow.replaceWith( '<img src="/media/img/icoblanco_abierto.png" width="17" height="10" alt="abrir" />' );
        //myarrow.replaceWith( '<img src="imagenes/icoblanco_abierto.png" width="17" height="10" alt="abrir" />' );
        return false;
      } else if (mysrc.search('abierto') != -1 ) {
        myarrow.replaceWith( '<img src="/media/img/icoblanco_cerrado.png" width="10" height="17" alt="cerrar" />' );
        //myarrow.replaceWith( '<img src="imagenes/icoblanco_cerrado.png" width="10" height="17" alt="cerrar" />' );
        return false;
      }
    }
  });
});
