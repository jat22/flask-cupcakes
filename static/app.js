
const BASE_URL = "http://127.0.0.1:5000/api"

function generateCupcakeHTML(cupcake){
	return `
		<li id=${cupcake.id}>
			<image class="cupcake-img" src=${cupcake.image}>
			${cupcake.flavor} - ${cupcake.rating} - ${cupcake.size}
			<button class="delete">X</button>
		</li>`
}

async function showCupcakes(){
	response = await axios.get(`${BASE_URL}/cupcakes`)
	const cupcakes = response.data.cupcakes

	for (let cupcake of cupcakes){
		const newCupcake = generateCupcakeHTML(cupcake)
		$("#cupcake-list").append(newCupcake)
	}
}

$('#cupcake-form').on('submit', async function(evt){
	evt.preventDefault();

	const flavor = $('#flavor').val();
	const size = $('#size').val();
	const rating = $('#rating').val();
	const image = $('#image').val();

	const response = await axios.post(`${BASE_URL}/cupcakes`, {
		flavor, size, rating, image
	});

	const cupcake = response.data.cupcake;

	const newCupcake = generateCupcakeHTML(cupcake);
	$('#cupcake-list').append(newCupcake);
	$('#cupcake-form').trigger('reset')
})

$('#cupcake-list').on('click', '.delete', async function(evt){
	evt.preventDefault();

	const $cupcake = $(evt.target).closest('li');
	const cupcakeId = $cupcake.attr("id");

	await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`)

	$cupcake.remove()
})

showCupcakes()