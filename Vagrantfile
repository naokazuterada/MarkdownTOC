# Your package name
PACKAGE = "UnitTesting-example"

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

$script = <<SCRIPT
export SUBLIME_TEXT_VERSION=$1
export PACKAGE="$2"
wget -O /home/vagrant/vagrant.sh https://raw.githubusercontent.com/randy3k/UnitTesting/master/sbin/vagrant.sh
chmod +x /home/vagrant/vagrant.sh
/home/vagrant/vagrant.sh provision
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"

    config.vm.define "st3" do |st3|
        st3.vm.provision "shell" do |s|
            s.inline = $script
            s.args = ["3", PACKAGE]
        end
    end
end
