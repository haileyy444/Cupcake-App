const BASE_URL = "http://127.0.0.1:5000/api";


function generateCupcake(cupcake) {
    console.log("generating cupcake");
    return `
        <div data-cupcake-id=${cupcake.id} class="col-sm-10 col-6 list-group-item">
        
        
            <li style="font-size: 20pt; color: navy; text-decoration: none;" class=" mt-3 row"  >
                <img class="col-sm-2 col-6 align" style="max-width: 200px; max-height: 200px;"
                    src="${cupcake.image}" 
                    alt="${cupcake.flavor} Cupcake">
                    </img>    
                <div class="col-sm-10 col-12 ">
                    <h1 class="mt-3"><b><a href="/api/cupcakes/${ cupcake.id }">${ cupcake.flavor }</a> </b> </h1>
                    <h3> ${cupcake.size} / ${cupcake.rating}/10</h3>
                </div>


                <button class="delete-button" style="color: white; border-color: white; font-size: 16pt; width: 5vw; background-color: red; display: block; margin: 0 auto;">X</button>

            </li>

            
        </div>
    `;
}

async function printCupcakeToList() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    for (let cupcakeInfo of response.data.cupcakes) {
        let newCupcake = $(generateCupcake(cupcakeInfo));
        console.log("adding cupcake to list");
        $("#cupcake-list").append(newCupcake);
    }
}

// new cupcake
$("#new-cupcake-form").on("submit", async function (e) {
    e.preventDefault();
    console.log("new cupcake");
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const newCupcake = await axios.post(`${BASE_URL}/cupcakes`, {flavor, rating, size, image});
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");

});


// delete cupcake
$("#cupcake-list").on("click", ".delete-button", async function (e) {
    e.preventDefault();


    // let $cupcake = $("#form-flavor").val();
    let $cupcake = $(this).closest('[data-cupcake-id]');
    let cupcakeID = $cupcake.attr("data-cupcake-id");

    try {
        console.log("delete cupcake");
        await axios.delete(`${BASE_URL}/cupcakes/${cupcakeID}`);
        $cupcake.remove(); // Remove the cupcake from the DOM
    } catch (error) {
        console.error("Error deleting cupcake:", error);
    }
});

$(printCupcakeToList);