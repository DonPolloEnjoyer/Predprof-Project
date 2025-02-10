
// async function getData() {
//     const url = "https://example.org/products.json";
//     try {
//       const response = await fetch(url);
//       if (!response.ok) {
//         throw new Error(`Response status: ${response.status}`);
//       }
  
//       const json = await response.json();
//       console.log(json);
//     } catch (error) {
//       console.error(error.message);
//     }
//   }
function GetById1(ElId){
  return document.getElementById(ElId)
}
function Search1(array, el){
  for (let i = 0; i < array.length; i++) {
    const n = array[i];
    if (n === el) {
        return true; break;
    }
  }
return false
}

GetById1("Vis1").onclick =
function PassText1(){
	let pass1 = GetById1("password");
	let v = GetById1("Vis1");
	if (pass1.type === "password") {
		pass1.type = "text"
    v.style.textDecoration = "none";
		v.style.backgroundColor = "greenyellow"
	} else if (pass1.type === "text") {
		pass1.type = "password"
		v.style.backgroundColor = "white"
    v.style.textDecoration = "line-through";
	}
}


