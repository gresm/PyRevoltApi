from __future__ import annotations
import re

from . import RequestThread

__all__ = [
    "make_request_to",
    "convert_url"
]


def _make_request(url: str, method: str, headers: dict):
    return RequestThread(url, method, headers)


def _is_arg(el: str, signature: str, regex: str):
    fixed_regex = regex.replace("~", signature)
    compiled = re.fullmatch(fixed_regex, el)
    return compiled is not None and compiled.string == el


def _fix_kwargs(kwargs: dict[str, str], fix_format: str = ":~"):
    new_kwargs = {}

    for ind in kwargs:
        new_kwargs[fix_format.replace("~", ind)] = kwargs[ind]

    return new_kwargs


def convert_url(local_url: str, global_url: str = "https://api.revolt.chat", *args: str,
                url_args: list[str] | tuple[str] = None, url_kwargs: dict[str, str] = None, __arg_signature: str = ":",
                __arg_regex: str = r"~\S+", __reverse_format: str = ":~", **kwargs: str):
    url_args = url_args if url_args else ()
    args += tuple(url_args)
    url_args = args

    url_kwargs = url_kwargs if url_kwargs else {}
    kwargs.update(url_kwargs)
    url_kwargs = _fix_kwargs(kwargs, __reverse_format)

    url_lst = local_url.split("/")
    found_ind = 0
    for ind in range(len(url_lst)):
        if _is_arg(url_lst[ind], __arg_signature, __arg_regex):
            cur_val = url_lst[ind]
            if len(url_args) > found_ind:
                cur_val = url_args[found_ind]
                found_ind += 1
            elif url_lst[ind] in url_kwargs:
                cur_val = url_kwargs[url_lst[ind]]

            url_lst[ind] = cur_val

    fixed_local_url = "/".join(url_lst)
    return global_url + fixed_local_url


def make_request_to(
        local_url: str, method: str, headers: dict, base_url: str = "https://api.revolt.chat", *args: str,
        url_args: list[str] | tuple[str] = None, url_kwargs: dict[str, str] = None,
        __arg_signature: str = ":", __arg_regex: str = r"~\S+", **kwargs):
    return _make_request(
        convert_url(local_url, url_args=url_args, url_kwargs=url_kwargs, __arg_signature=__arg_signature,
                    __arg_regex=__arg_regex, global_url=base_url, *args, **kwargs),
        method, headers
    )
