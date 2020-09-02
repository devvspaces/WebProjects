import string
import random
import hashlib

def encrypt_string(hash_string):
    sha_signature = hashlib.md5(hash_string.encode()).hexdigest()
    return sha_signature


def random_str_gen(size, chars=string.ascii_lowercase+string.digits):
	return ''.join([random.choice(chars) for _ in  range(size)])

def create_tid(instance, new_slug=None):
	#create unique todo identifier variable
	if new_slug:
		tid=slugify(new_slug)
	else:
		tid=encrypt_string(random_str_gen(5))
	klass=instance.__class__
	#if tid already exist
	qs_exists=klass.objects.filter(tid=tid).exists()
	if qs_exists:
		new_tid=encrypt_string(random_str_gen(5))
		return create_slug(instance, new_tid)
	return tid