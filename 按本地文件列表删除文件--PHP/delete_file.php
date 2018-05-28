<?php
class upyun{
	const END_POINT = "http://v0.api.upyun.com";
	private $bucketname;
    private $username;
    private $password;
	private $isasync;

	public function __construct($bucketname, $username, $password, $isasync){

		$this->bucketname = $bucketname;
        $this->username = $username;
        $this->password = $password;
        $this->isasync = $isasync;

	}

	public function del($dstpath){

		$uri = "/{$this->bucketname}$dstpath";
		$date = gmdate('D, d M Y H:i:s \G\M\T');
		$signature = base64_encode(hash_hmac("sha1", "DELETE&$uri&$date", md5("{$this->password}"), true));
		$header = array("Authorization:UPYUN {$this->username}:$signature", "Date:$date", "x-upyun-async:{$this->isasync}");

		$ch = curl_init(self::END_POINT.$uri);
		curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_POST, 1);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
		$rsp_body = curl_exec($ch);
		$rsp_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		curl_close($ch);
		return array("code"=>$rsp_code,"msg"=>$rsp_body);

	}

	public function delfile($path){
		$fh = fopen($path,"rb") or die("Unable to open file.");
		while(!feof($fh)){
			$fileline = fgets($fh);
			$fileline = str_replace("\n", "", $fileline);
			$resdel = self::del($fileline);
			if($resdel["code"] == 200){
				file_put_contents("delsucc.txt",$fileline."\n", FILE_APPEND);
				echo "DELETE ".$fileline." SUCCESS\n";
			}else{
				file_put_contents("delfail.txt",$fileline."\ncode: ".$resdel["code"]." message: ".$resdel["msg"]."\n\n", FILE_APPEND);
				echo "DELETE ".$fileline." FAILED\n";
			}
		}
	}

}

$upyun = new upyun("bucket", "user", "password", false);

$upyun->delfile("del.txt");



?>