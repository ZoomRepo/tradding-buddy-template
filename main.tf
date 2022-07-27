provider "aws" {
  region     = "eu-west-2"
  access_key = "AMAZON ACCESS KEY"
  secret_key = "AMAZON SECRET KEY"
}

# 1. Create VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "Test Instance"
  }
}


# 2. Create Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "Test Instance"
  }
}

# 3. Create Custom Route Table
resource "aws_route_table" "example" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "Test Instance"
  }
}

# 4. Create a Subnet
resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"

  availability_zone = "eu-west-2a"
  tags = {
    Name = "Test Instance"
  }
}

# 5. Associate Subnet with Route Table
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.example.id
}

# 6. Create Security Group to allow port 22, 80 and 443
resource "aws_security_group" "allow_web" {
  name        = "allw_web_traffic"
  description = "Allow inbound Web traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_web_traffic"
  }
}

# 7. Create a Network Interface with an IP in the Subnet that was Created in step 4
resource "aws_network_interface" "test-web-server" {
  subnet_id       = aws_subnet.main.id
  private_ips     = ["10.0.1.50"]
  security_groups = [aws_security_group.allow_web.id]
}

# 8. Assign an Elastic IP to the Network Interfacecreated in steap 7
resource "aws_eip" "one" {
  vpc                       = true
  network_interface         = aws_network_interface.test-web-server.id
  associate_with_private_ip = "10.0.1.50"
  depends_on = [
    aws_internet_gateway.gw
  ]
}


# 9. Create an Ubuntu Server and install / enable apache2
resource "aws_instance" "foo" {
  ami               = "ami-0fdf70ed5c34c5f52" # us-west-2
  instance_type     = "t2.micro"
  availability_zone = "eu-west-2a"
  key_name          = "main-key"

  network_interface {
    network_interface_id = aws_network_interface.test-web-server.id
    device_index         = 0
  }

  user_data = <<-EOF
                #!/bin/bash
                sudo apt update && sudo apt upgrade -y
                sudo apt install apache2 -y
                sudo apt install python3
                sudo apt install python3-pip
                sudo apt install software-properties-common -y
                sudo add-apt-repository ppa:deadsnakes/ppa
                sudo systemctl start apache2
                
                sudo bash -c 'echo Apache 2 Web Server running Python Version: \"$(python3 -V 2>&1)\" > /var/www/html/index.html'
                
                cd /home/ubuntu/
                git clone https://zoomrepo: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@github.com/ZoomRepo/ebay-scanner.git
                cd ebay-scanner              
                pip3 install -r requirements.txt
                python3 ebay_scanner/main.py
                EOF
  tags = {
    Name = "Web Scrapper Service"
  }
}
