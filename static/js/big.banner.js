$(document).ready(function(){
  //Se eliminana las clases far-away de los botones de abrir y cerrar y el banner grande para que sean visibles por el usuario
  $('#contenedor-banner-principal .far-away').removeClass('far-away');
  
  //Se esconden las opciones colapsadas
  if ( $.cookie("cookie_bigbaner") != "close" ) {
    $('#contenedor-banner-principal-wrapper-colapsado').hide();
    $('#contenedor-banner-principal #abrir-banner').hide();
    $.cookie("cookie_bigbaner", "open", { expires: 14, domain: 'www.uji.es' });
  } else {
    $('#contenedor-banner-principal-wrapper-expandido').hide();
    $('#contenedor-banner-principal #cerrar-banner').hide();
  }
  
  //Se esconden las opciones colapsadas
  
  
  //Especificamos los dos procesos de cierre y apertura del baner grande
  $('#contenedor-banner-principal #cerrar-banner').click(function(){
    //$('#contenedor-banner-principal #banner-principal-fecha').hide(300);
    $('#contenedor-banner-principal-wrapper-expandido').animate({
      height: 'toggle'
    }, 500, function() {
      $('#contenedor-banner-principal #cerrar-banner').hide(0, function() {
        $('#contenedor-banner-principal #abrir-banner').show(0,function(){
          $('#contenedor-banner-principal-wrapper-colapsado').animate({
            height: 'toggle'
          }, 500);
          $.cookie("cookie_bigbaner", "close", { expires: 14, domain: 'www.uji.es' });
        });
      });
    });
    return false;
  });
  
  $('#contenedor-banner-principal #abrir-banner').click(function(){
    $('#contenedor-banner-principal-wrapper-colapsado').animate({
      height: 'toggle'
    }, 500, function() {
      $('#contenedor-banner-principal #abrir-banner').hide(0, function() {
        $('#contenedor-banner-principal #cerrar-banner').show(0,function(){
          $('#contenedor-banner-principal-wrapper-expandido').animate({
            height: 'toggle'
          }, 500, function(){
            //$('#contenedor-banner-principal #banner-principal-fecha').show(100);
            $.cookie("cookie_bigbaner", "open", { expires: 14, domain: 'www.uji.es'});
          });
        });
      });
    });
    return false;
  });


         $(function() {
             $("#slideshow1").hover(
                 function() { $("#controles1").fadeIn(); },
                 function() { $("#controles1").fadeOut(); }
             );
             $("#slideshow2").hover(
                 function() { $("#controles2").fadeIn(); },
                 function() { $("#controles2").fadeOut(); }
             );
             $("#slides1").cycle({
                 fx:     "fade",
                 speed:   400,
                 timeout: 4000,
                 next:   "#next1",
                 prev:   "#prev1"
             });
             $("#slides2").cycle({
                 fx:     "fade",
                 speed:   400,
                 timeout: 4000,
                 next:   "#next2",
                 prev:   "#prev2"
             });
         });

});
