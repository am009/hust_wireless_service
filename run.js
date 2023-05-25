
import * as std from "std";

std.loadScript("security.js");

function encryptedPassword(password){

	//var passwordEncode = encodeURIComponent(encodeURIComponent(password)).split("").reverse().join("");
	var passwordEncode = password.split("").reverse().join("");
	//老的加密算法有问题，使用新的实现方法
	 var publicKeyExponent='10001';
	 var publicKeyModulus='94dd2a8675fb779e6b9f7103698634cd400f27a154afa67af6166a43fc26417222a79506d34cacc7641946abda1785b7acf9910ad6a0978c91ec84d40b71d2891379af19ffb333e7517e390bd26ac312fe940c340466b4a5d4af1d65c3b5944078f96a1a51a5a53e4bc302818b7c9f63c4a1b07bd7d874cef1c3d4b2f5eb7871';
	 window.RSAUtils.setMaxDigits(400);
	 var key = new window.RSAUtils.getKeyPair(publicKeyExponent, "", publicKeyModulus); 
	 var passwordEncry = window.RSAUtils.encryptedString(key,passwordEncode);//这里要对字符串进行反转，否则解密的密码是反的
	 
	 return passwordEncry;
}
// var passwordMac = password+">"+macString;
var password = std.in.getline();

password = encryptedPassword(password)
std.out.puts(password);
std.out.flush()
