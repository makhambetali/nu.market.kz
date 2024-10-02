const buttons = document.querySelectorAll(".change_language_button");
const textLogo = document.querySelector(".logo");
const textPost_an_item_link = document.querySelector(".post_an_item_link");
const textSignin_link = document.querySelector(".signin_link");
const textProfile_link = document.querySelector(".profile_link");
const textLanguage_button = document.querySelector(".language_button");
const textEnglish_button = document.querySelector(".english_button");
const textRussian_button = document.querySelector(".russian_button");
const textSignout_link = document.querySelector(".signout_link");
const textRemove_button = document.querySelector(".remove_button");

const data = {
	english: {
		logo: "LOGO",
		post_an_item_link: "Post an Item",
		signin_link: "Sign In",
		profile_link: "Profile",
		language_button: "Language",
		english_button: "English",
		russian_button: "Russian",
		signout_link: "Signout",
		remove_button: "Remove",
	},
	russian: {
		logo: "ЛОГО",
		post_an_item_link: "Подать объявление",
		signin_link: "Войти",
		profile_link: "Профиль",
		language_button: "Язык",
		english_button: "Английский",
		russian_button: "Руский",
		signout_link: "Выйти",
		remove_button: "Убрать",
	},
};

function updateLanguage(language) {
	if (textLogo) textLogo.textContent = data[language].logo;
	if (textPost_an_item_link)
		textPost_an_item_link.textContent = data[language].post_an_item_link;
	if (textSignin_link)
		textSignin_link.textContent = data[language].signin_link;
	if (textProfile_link)
		textProfile_link.textContent = data[language].profile_link;
	if (textLanguage_button)
		textLanguage_button.textContent = data[language].language_button;
	if (textEnglish_button)
		textEnglish_button.textContent = data[language].english_button;
	if (textRussian_button)
		textRussian_button.textContent = data[language].russian_button;
	if (textSignout_link)
		textSignout_link.textContent = data[language].signout_link;
	if (textRemove_button)
		textRemove_button.textContent = data[language].remove_button;
}

document.addEventListener("DOMContentLoaded", () => {
	const savedLanguage = localStorage.getItem("language") || "russian";
	updateLanguage(savedLanguage);
});

buttons.forEach((button) => {
	button.addEventListener("click", () => {
		const attr = button.getAttribute("language");
		localStorage.setItem("language", attr);
		updateLanguage(attr);
	});
});
