from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import json
import string
import collections


def index(request):
    context = {'hello': 'hello'}
    return render_to_response('base.html', context, context_instance=RequestContext(request))


def encrypt_decrypt(request):
    text = request.POST.get("text")
    offset = int(request.POST.get("offset"))
    mode = int(request.POST.get("mode"))
    result_text = ''
    for letter in text:
        if letter.isalpha():
            num = ord(letter)
            if mode == 1:
                num += offset
            elif mode == 2:
                num -= offset
            if letter.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif letter.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            result_text += chr(num)
        else:
            result_text += letter

    context = {'result_text': result_text}
    return HttpResponse(json.dumps(context))


def frequencies(request):
    text = request.POST.get("text")
    count_letters = len([letter for letter in text.lower() if letter in string.ascii_lowercase])
    freq = collections.OrderedDict()
    for letter in string.ascii_lowercase:
        freq[letter] = 0
    for letter in text.lower():
        if letter in string.ascii_lowercase:
            freq[letter] += 1
    crack = get_min_chi_square(freq, count_letters)
    for key, value in freq.items():
        fr = float(value) / count_letters * 100
        freq[key] = fr
    freq1 = freq.items()
    freq1.insert(0, ['Element', 'Density'])
    context = {'freq': freq1, 'crack': crack}
    return HttpResponse(json.dumps(context))


def get_min_chi_square(freq, count_letters):
    expected = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749,
                7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.361, 0.150, 1.974, 0.074]
    chi_squares = []
    for offset in range(1, 27):
        ind = offset - 1
        chi_sum = 0
        for key, value in freq.items():
            exp = expected[ind] / 100 * count_letters
            chi = (value - exp) * (value - exp) / exp
            chi_sum += chi
            ind += 1
            if ind > 25:
                ind = 0
        chi_squares.append(chi_sum)
    return 26 - chi_squares.index(min(chi_squares))