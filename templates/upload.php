<?php

if(count($_FILES['files']['name'])) {
	$i = 0;
	foreach ($_FILES['files']['name'] as $file) {
		$img = "static/uploads/".$file;
		move_uploaded_file($_FILES['files']['tmp_name'][$i], $img);
		chmod( $img , 0777 );
	}
}
 ?>
