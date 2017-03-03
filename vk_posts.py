

def form_vk_post_link(page_id, post_id):
    return "https://vk.com/wall%d_%d" % (page_id, post_id)


def strip_irrelevant_post_info(raw_post):
    return {'date': raw_post['date'],
            'text': raw_post['text'],
            'link': form_vk_post_link(raw_post['from_id'], raw_post['id']),
            }


def strip_vk_posts(post_list):
    return [strip_irrelevant_post_info(post) for post in post_list]

if __name__ == '__main__':
    args = get_argument_parser()
    source_ids = load_data(agrs.infile)
    posts = get_vk_posts(source_ids)
    python_posts = filter_posts(posts, is_python_post)
    python_stripped_posts = strip_vk_posts(python_posts)
    save_data(python_stripped_posts)
