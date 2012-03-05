$(document).ready(function(){
  //Se eliminana las clases far-away de los botones de abrir y cerrar y el banner del contenido para que sean visibles por el usuario
  $('#contenedor-banner-contenido .far-away').removeClass('far-away');
  
  //Se esconden las opciones colapsadas
  if ( $.cookie("cookie_midbaner") != "close" ) {
    $('#contenedor-banner-contenido .colapsado').hide();
    $('#contenedor-banner-contenido #abrir-banner-servicio').hide();
    $.cookie("cookie_midbaner", "open", { expires: 14, domain: 'www.uji.es' });
  } else {
    $('#contenedor-banner-contenido .expandido').hide();
    $('#contenedor-banner-contenido #cerrar-banner-servicio').hide();
  }
  
  //Especificamos los dos procesos de cierre y apertura del baner grande
  $('#contenedor-banner-contenido #cerrar-banner-servicio').click(function(){
    $('#contenedor-banner-contenido #banner-contenido-fecha').hide(300);
    $('#contenedor-banner-contenido .expandido').animate({
      height: 'toggle'
    }, 500, function() {
      $('#contenedor-banner-contenido #cerrar-banner-servicio').hide(0, function() {
        $('#contenedor-banner-contenido #abrir-banner-servicio').show(0,function(){
          $('#contenedor-banner-contenido .colapsado').animate({
            height: 'toggle'
          }, 500, function(){
            $('#contenedor-banner-contenido #banner-contenido-fecha').show(100);
            $.cookie("cookie_midbaner", "close", { expires: 14, domain: 'www.uji.es' });
            recalcula_alturas();
          });
        });
      });
    });
    return false;
  });
  $('#contenedor-banner-contenido #abrir-banner-servicio').click(function(){
    $('#contenedor-banner-contenido .colapsado').animate({
      height: 'toggle'
    }, 500, function() {
      $('#contenedor-banner-contenido #abrir-banner-servicio').hide(0, function() {
        $('#contenedor-banner-contenido #cerrar-banner-servicio').show(0,function(){
          $('#contenedor-banner-contenido .expandido').animate({
            height: 'toggle'
          }, 500, function(){
            $('#contenedor-banner-contenido #banner-contenido-fecha').show(100);
            $.cookie("cookie_midbaner", "open", { expires: 14, domain: 'www.uji.es' });
            recalcula_alturas();
          });
        });
      });
    });
    return false;
  });
});