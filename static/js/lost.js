$(document).ready(function() {
    $(".logout").hide();
  (function() {             //Fetch All the data from DB
      $.ajax({
          url: '/fetch/',
          method: 'GET',
          dataType: 'json',
          data: {
            statusType: 'LOST'
          },
          success: function(data) {
              userAdmin = data.usertype;
              data = data.fetched_data;
              //console.log(data);
              //console.log(userAdmin)
              const jsonData = JSON.parse(data);
              // Reverse the jsonData array
              jsonData.reverse();
               // Generate cards based on data
               const cardContainer = $('#card-container'); // Container for cards

               if (userAdmin === true){
                $(".recentfound").text("Recently LOST (ADMIN MODE)");
                $(".logout").show();
                }
                 else{
                    $(".logout").hide();
                 }

               jsonData.forEach(item => {
                   const card = `
                   <div class="card cardmain" id="cardd" ${item.status === 1 ? 'style="background-color:  #c1b5c1;"' : ''}>
                           <img src="/static/items/lostImg/${item.id}.${item.ext}/" class="card-img-top custom-img-size" alt="Item Image"><hr>
                           <div class="card-body">
                               <h4 class="card-title">Item name: ${item.itemName}</h4>
                               <p class="card-text">Owner Name: ${item.name}</p>
                               <p class="card-text">Lost At: ${item.location}</p>
                               <p class="card-text">Lost On: ${item.date}</p>
                               <p class="card-text">Contact Me: ${item.contact}</p>
                               ${
                                  item.status === 1
                                      ? '<p style="color: green; font-size: large;">The Item Has Been Found by The Owner</p>'
                                      : `<button class="btn btn-success" type="submit" onclick="markFound('${item.id}')">Mark As Found</button>`
                              }
                              ${
                                userAdmin === true
                                    ? `<button class="btn btn-danger" type="submit" onclick="deleteItem('${item.id}') ">Delete</button>`
                                    : ''
                              }
                              ${
                                userAdmin === true && item.status === 1
                                    ? `<button class="btn btn-info" type="submit" onclick="revertItem('${item.id}') ">Revert</button>`
                                    : ''
                              }
                           </div>
                       </div>
                   `;
                   cardContainer.append(card);
               });

          },
          error: function(xhr, status, error) {
              console.error('Error fetching data:', error);
          }
      });
  })();
});

function markFound(itemId) {
  $.ajax({
      url: '/markFound/',
      method: 'POST',
      data: {
        itemId: itemId,
        statusType: 'LOST'
      },
      success: function(data) {
          //console.log(data);
          location.reload();
      },
      error: function(xhr, status, error) {
          console.error('Error Sending Request', error);
      }
  });
}

function deleteItem(itemId){
    $.ajax({
        url: '/delete/',
        method: 'POST',
        data: {
            itemId: itemId,
            statusType: 'LOST'
          },
        success: function(data) {
            //console.log(data);
            location.reload();
        },
        error: function(xhr, status, error) {
            console.error('Error Sending Request', error);
        }
    });
}

function revertItem(itemId){
    $.ajax({
        url: '/revert/',
        method: 'POST',
        data: {
            itemId: itemId,
            statusType: 'LOST'
          },
        success: function(data) {
            //console.log(data);
            location.reload();
        },
        error: function(xhr, status, error) {
            console.error('Error Sending Request', error);
        }
    });
}
