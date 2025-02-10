

GetById1("CreateAc1").onclick = 

function Soz2(){
	// console.log()
  let log1 = GetById1("username").value;
  
  let pass1 = GetById1("password").value;
  
		if ((pass1.length < 8) || (Search1(pass1, " "))) {
			console.log(Boolean(Search1(pass1, " ")));
			GetById1("CreateAc1ptext").innerHTML = "Ошибка";
            GetById1("password").style.borderColor = "red";
			GetById1("Passwarn1").innerHTML = "Пароль должен составлять минимум 8 символов\n"+
			"(Ваша длина: "+ pass1.length +" ). Без содержания пробелов.";
		} else {
			GetById1("password").style.borderColor = "greenyellow";
		}
		if (log1 === ''){
			GetById1("CreateAc1ptext").innerHTML = "Ошибка";
			GetById1("username").style.borderColor = "red";
            GetById1("Passwarn1").innerHTML = " Введите логин."

		} else {
			GetById1("username").style.borderColor = "greenyellow";
		}
		if (!((pass1.length < 8) || (Search1(pass1, " ")) || log1 === '' )){
		GetById1("password").type = "password";
		GetById1("Vis1").remove();
		GetById1("CreateAc1ptext").innerHTML = "Создание";
        GetById1("Passwarn1").innerHTML = "";
		GetById1("CreateAc1").type = "sumbit"
		// GetById1("rform").method="post";
		// GetById1("rform").action="/auth/reg";
		// SendReg1(log1, pass1);
		}
}

// function SendReg1(log, pass){
// 	let a = new Request({login: log, password: pass})
// 	// fetch("http://192.168.1.24:3306", a)
	
	
// }

