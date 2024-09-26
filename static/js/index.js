const length_slice = (el, max_len) => {
    if (el.value.length >= max_len-1) {
      el.value = el.value.slice(0, max_len);
    }
  }

  IMask(
    document.querySelector('.currency-input'),
    {
        mask: '₸ num',
        blocks: {
            num: {
                mask: Number,
                thousandsSeparator: '.'
            }
        }
    }
);