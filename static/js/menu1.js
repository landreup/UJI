$(document).ready(function(){
  //Construimos el menu expandido a partir del colapsado que es el que aparece por defecto si no se activa js
  $('#menu-primario').prepend('<div class="expandido" />');
  $('#menu-primario .expandido').html( $('#menu-primario .colapsado ul').clone() );
  var subniveles = $('#menu-primario .expandido .subnivel').removeClass('no-activo');
  var nivel = $('#menu-primario .expandido ul.nivel li');
  $(nivel).each(function(index) {
    $(this).append(subniveles[index]);
  });
  
  //Se eliminana las clases far-away de los botones de abrir y cerrar menu para uqe sean visibles por el usuario
  $('#menu-primario .far-away').removeClass('far-away');
  
  //Añadimos el vento de click para que en el menú colapasado se muestren los elementos de segundo nivel ¿?
  $('#menu-primario .colapsado ul.nivel li').click(function(){
    $('#menu-primario .colapsado ul.nivel li.activo').removeClass('activo');
    $(this).addClass('activo');
    $('#menu-primario .colapsado ul.subnivel').removeClass('activo');
    $('#menu-primario .colapsado ul.subnivel').addClass('no-activo');
    $('#menu-primario .colapsado ul.subnivel:eq(' + $('#menu-primario .colapsado ul.nivel li').index($(this)) + ')').removeClass('no-activo').addClass('activo');
    //Marcamos tambien el menu expandido ¿?
    $('#menu-primario .expandido ul.nivel > li.activo').removeClass('activo');
    $('#menu-primario .expandido ul.nivel > li:eq(' + $('#menu-primario .colapsado ul.nivel li').index($(this)) + ')').addClass('activo');
    if ( $(this).find('a').attr('href') == '#' ) {
      return false;
    }
  });
  
  //Se esconden las colapsadas del menu
  if ( $.cookie("cookie_menu1") != "close" ) {
    $.cookie("cookie_menu1", "open", { expires: 14, domain: 'www.uji.es' });
    $('#menu-primario .colapsado').hide();
    $('#menu-primario #abrir-menu').hide();
  } else {
    $('#menu-primario .expandido').hide();
    $('#menu-primario #cerrar-menu').hide();
  }
  //Especificamos los dos procesos de cierre y apertura del menú
  $('#menu-primario #cerrar-menu').click(function(){
    $('#menu-primario .expandido').animate({
      height: 'toggle'
    }, 500, function() {
      $('#menu-primario #cerrar-menu').hide(0, function() {
          $('#menu-primario #abrir-menu').show(0);
      $('#menu-primario .colapsado').animate({
        height: 'toggle'
      }, 500);
      $.cookie("cookie_menu1", "close", { expires: 14, domain: 'www.uji.es' });
      });
    });
    return false;
  });
  
  $('#menu-primario #abrir-menu').click(function(){
    $('#menu-primario .colapsado').animate({
      height: 'toggle'
    }, 500, function() {
      $('#menu-primario #abrir-menu').hide(0, function() {
        $('#menu-primario #cerrar-menu').show(0);
        $('#menu-primario .expandido').animate({
          height: 'toggle'
        }, 500);
        $.cookie("cookie_menu1", "open", { expires: 14, domain: 'www.uji.es' });
      });
    });
    return false;
  });
});
