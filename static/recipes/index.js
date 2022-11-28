// const csrftoken = Cookies.get('csrftoken');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
console.log(csrftoken);

// function editMe(el) {
//     var editid = el.dataset['id'];
//     //console.log(editid);

//     fetch('/getpost/' + editid)
//     .then(response => response.json())
//     .then((data) => {

//         var userid = data.id;
//         var jsonresponse = data.jsonreply;
//         var jsonbody = jsonresponse.body;
//         var jsonID = jsonresponse.id;
//         var parent = document.getElementById("card-" + jsonID);
//         parent.querySelector('.card-subtitle').style.display = "none";
//         parent.querySelector('.card-text').style.display = "none";
//         parent.querySelector('.card-link-edit').style.display = "none";
//         var cardlinks = parent.getElementsByClassName("card-link");
//         for (var i = 0; i < cardlinks.length; i++) {
//             cardlinks.item(i).style.display = "none";
//         }
        
//         const f = document.getElementById('form-' + editid);

//         const k = document.createElement("textarea");
//         k.setAttribute('type', "textarea");
//         k.setAttribute('value', jsonbody);
//         k.id = "textarea-" + jsonID;
//         k.innerHTML = jsonbody;

//         const s = document.createElement("input");
//         s.setAttribute('type', 'Submit');
//         s.setAttribute('value', "Submit");
//         s.id = "submit-" + jsonID;
//         s.setAttribute("onclick", `update_post(${jsonID})`);
//         s.classList.add("btn", "btn-primary");

//         f.appendChild(k);
//         f.appendChild(s);
//     });
// }

// function update_post(id) {
//     const element = document.getElementById('form-' + id);
//     element.addEventListener('submit', event => {
//         event.preventDefault();
//         // actual logic, e.g. validate the form
//         const newbody = document.getElementById("textarea-" + id).value;
//         console.log(newbody);

//         // console.log(newbody);

//         fetch('/getpost/' + id, {
//             method: 'PUT',
//             headers: {'X-CSRFToken': csrftoken},
//             mode: 'same-origin', // Do not send CSRF token to another domain.
//             body: JSON.stringify(newbody)
//         })
//         .then(response => response.json())
//         .then(result => {
//             // Print result
//             console.log(result);
//             var parent = document.getElementById("card-" + id);
//             parent.querySelector('.card-subtitle').style.display = "block";
//             parent.querySelector('.card-text').style.display = "block";
//             parent.querySelector('.card-text').innerHTML = newbody;
//             parent.querySelector('.card-link-edit').style.display = "block";
//             var cardlinks = parent.getElementsByClassName("card-link");
//             for (var i = 0; i < cardlinks.length; i++) {
//                 cardlinks.item(i).style.display = "block";
//             }
            
//             const f = document.getElementById('form-' + id);
//             removeAllChildNodes(f);

//         });
//     });
// }

function followMe(el) {
    likeid = el.dataset['id'];
    var obj;
    var pathArray = window.location.pathname.split('/');
    var userToFollow = pathArray[2];
    var follower = el.dataset['id'];
    var followed = userToFollow;

    fetch('/api/user/follow/' + follower, {
        method: 'PUT',
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          'X-CSRFToken': csrftoken
        },
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({
             followed: followed
        })
    })    
    .then(res => res.json())
    .then(data => obj = data)
    .then(() => console.log(obj))
    .then(() => update(likeid, obj.reply))
    .then(() => update("followedCount", "Followers: " + obj.followedCount))
    // .then(() => update("followerCount", "Following: " + obj.followerCount))

}


function likebutton(el) {
    likeid = el.dataset['id'];
    likeuser = el.dataset['currentuser'];
    var obj;
    
    fetch('/api/recipe/' + likeid, {
        method: 'PUT',
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          'X-CSRFToken': csrftoken
        },
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({
             id: likeid,
             user: likeuser
        })
    })    
    .then(res => res.json())
    .then(data => obj = data)
    .then(() => update(likeid, obj.likes + " Likes"))
  }

  function savebutton(el) {
    saveid = el.dataset['id'];
    saveuser = el.dataset['currentuser'];
    var obj;
    
    
    fetch('/api/bookmark/' + saveid, {
        method: 'PUT',
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          'X-CSRFToken': csrftoken
        },
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({
             id: saveid,
             user: saveuser
        })
    })    
    .then(res => res.json())
    .then(data => obj = data)
    .then(() => console.log(obj))
    .then(() => update("save-" + saveid, obj.saved))
  }

  function update(id, string) {
    document.getElementById(id).innerHTML = string;
  }

  function removeAllChildNodes(parent) {
    if (parent.hasChildNodes) {
      while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
      }
    }
  }


  