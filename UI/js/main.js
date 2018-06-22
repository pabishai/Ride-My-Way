/** 
 * Main project javascript file
 * 
* */

/**
 * open collapsable divs
 */

//Get all elements with the class open_collapsable.
var collapseButton = document.getElementsByClassName("open_collapsable");

//loop through the elements. 
for (var i = 0; i < collapseButton.length; i++) {

    //add an event listener for clicks
    collapseButton[i].addEventListener("click", function() {
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
} 

/**
 *  navigation overlay
 */

/** open overlay */

 //Get hamburger menu with id #menu_link
 var openMenu = document.getElementById("menu_link");

 //add click event listener
 openMenu.addEventListener("click", function(){
     //get menu overlay
     menu = document.getElementById("menu");
     
     //expand width to 100%
     menu.style.width = "100%";
 });

 /** Close Overlay */
 
 //get all elements with class .close
 var closeMenu = document.getElementsByClassName("close");

 //loop through the elements
 for(var i=0; i<closeMenu.length; i++){
     //add event listener to each element
     closeMenu[i].addEventListener("click",function(){
        //get menu overlay
        menu = document.getElementById("menu");
     
        //close
        menu.style.width = "0";
     });
 }

 

