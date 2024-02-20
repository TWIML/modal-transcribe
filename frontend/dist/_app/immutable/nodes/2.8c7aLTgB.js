import { s as safe_not_equal, n as noop, o as onMount } from "../chunks/scheduler.fAU1PGX9.js";
import { S as SvelteComponent, i as init, o as empty, a as insert_hydration, d as detach, e as element, c as claim_element, g as get_svelte_dataset, b as children, t as text, s as space, f as claim_text, h as claim_space, m as attr, j as append_hydration, k as set_data, p as create_component, q as claim_component, r as mount_component, l as transition_in, n as transition_out, u as destroy_component } from "../chunks/index.yutBPzth.js";
import { h as hooks, e as ensure_array_like, u as update_keyed_each, d as destroy_block } from "../chunks/moment.nDPJJoOf.js";
async function load({ params, fetch: fetch2 }) {
  const podcastId2 = "twiml-ai-podcast";
  const res = await fetch2(`/api/podcast/${podcastId2}`);
  const data = await res.json();
  return { data: data["pod_metadata"] };
}
const _page = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  load
}, Symbol.toStringTag, { value: "Module" }));
function get_each_context(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[3] = list[i][0];
  child_ctx[4] = list[i][1];
  return child_ctx;
}
function create_else_block(ctx) {
  let p;
  let textContent = "Loading episodes...";
  return {
    c() {
      p = element("p");
      p.textContent = textContent;
    },
    l(nodes) {
      p = claim_element(nodes, "P", { ["data-svelte-h"]: true });
      if (get_svelte_dataset(p) !== "svelte-xjbjzk")
        p.textContent = textContent;
    },
    m(target, anchor) {
      insert_hydration(target, p, anchor);
    },
    p: noop,
    d(detaching) {
      if (detaching) {
        detach(p);
      }
    }
  };
}
function create_if_block(ctx) {
  let ul;
  let each_blocks = [];
  let each_1_lookup = /* @__PURE__ */ new Map();
  let each_value = ensure_array_like(Object.entries(
    /*episodes*/
    ctx[0]
  ).sort(func));
  const get_key = (ctx2) => (
    /*episode*/
    ctx2[4].guid_hash
  );
  for (let i = 0; i < each_value.length; i += 1) {
    let child_ctx = get_each_context(ctx, each_value, i);
    let key = get_key(child_ctx);
    each_1_lookup.set(key, each_blocks[i] = create_each_block(key, child_ctx));
  }
  return {
    c() {
      ul = element("ul");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
    },
    l(nodes) {
      ul = claim_element(nodes, "UL", {});
      var ul_nodes = children(ul);
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].l(ul_nodes);
      }
      ul_nodes.forEach(detach);
    },
    m(target, anchor) {
      insert_hydration(target, ul, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(ul, null);
        }
      }
    },
    p(ctx2, dirty) {
      if (dirty & /*Object, episodes, formatDate, podcastId*/
      3) {
        each_value = ensure_array_like(Object.entries(
          /*episodes*/
          ctx2[0]
        ).sort(func));
        each_blocks = update_keyed_each(each_blocks, dirty, get_key, 1, ctx2, each_value, each_1_lookup, ul, destroy_block, create_each_block, null, get_each_context);
      }
    },
    d(detaching) {
      if (detaching) {
        detach(ul);
      }
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].d();
      }
    }
  };
}
function create_each_block(key_1, ctx) {
  let li;
  let span0;
  let t0_value = (
    /*episode*/
    ctx[4].episode_number + ""
  );
  let t0;
  let t1;
  let t2;
  let a;
  let t3_value = (
    /*episode*/
    ctx[4].title + ""
  );
  let t3;
  let a_href_value;
  let t4;
  let span1;
  let t5;
  let t6_value = (
    /*formatDate*/
    ctx[1](
      /*episode*/
      ctx[4].publish_date
    ) + ""
  );
  let t6;
  let t7;
  let t8_value = (
    /*episode*/
    ctx[4].transcribed ? "📃 " : "  "
  );
  let t8;
  let t9;
  return {
    key: key_1,
    first: null,
    c() {
      li = element("li");
      span0 = element("span");
      t0 = text(t0_value);
      t1 = text(" |");
      t2 = space();
      a = element("a");
      t3 = text(t3_value);
      t4 = space();
      span1 = element("span");
      t5 = text("| ");
      t6 = text(t6_value);
      t7 = space();
      t8 = text(t8_value);
      t9 = space();
      this.h();
    },
    l(nodes) {
      li = claim_element(nodes, "LI", { class: true });
      var li_nodes = children(li);
      span0 = claim_element(li_nodes, "SPAN", { class: true });
      var span0_nodes = children(span0);
      t0 = claim_text(span0_nodes, t0_value);
      t1 = claim_text(span0_nodes, " |");
      span0_nodes.forEach(detach);
      t2 = claim_space(li_nodes);
      a = claim_element(li_nodes, "A", { href: true, class: true });
      var a_nodes = children(a);
      t3 = claim_text(a_nodes, t3_value);
      a_nodes.forEach(detach);
      t4 = claim_space(li_nodes);
      span1 = claim_element(li_nodes, "SPAN", { class: true });
      var span1_nodes = children(span1);
      t5 = claim_text(span1_nodes, "| ");
      t6 = claim_text(span1_nodes, t6_value);
      span1_nodes.forEach(detach);
      t7 = claim_space(li_nodes);
      t8 = claim_text(li_nodes, t8_value);
      li_nodes.forEach(detach);
      t9 = claim_space(nodes);
      this.h();
    },
    h() {
      attr(span0, "class", "text-gray-400");
      attr(a, "href", a_href_value = `/podcast/${podcastId}/episode/${/*episode*/
      ctx[4].episode_number}`);
      attr(a, "class", "text-blue-900 no-underline hover:underline");
      attr(span1, "class", "text-gray-400");
      attr(li, "class", "px-6 py-2 w-full rounded-t-lg");
      this.first = li;
    },
    m(target, anchor) {
      insert_hydration(target, li, anchor);
      append_hydration(li, span0);
      append_hydration(span0, t0);
      append_hydration(span0, t1);
      append_hydration(li, t2);
      append_hydration(li, a);
      append_hydration(a, t3);
      append_hydration(li, t4);
      append_hydration(li, span1);
      append_hydration(span1, t5);
      append_hydration(span1, t6);
      append_hydration(li, t7);
      append_hydration(li, t8);
      insert_hydration(target, t9, anchor);
    },
    p(new_ctx, dirty) {
      ctx = new_ctx;
      if (dirty & /*episodes*/
      1 && t0_value !== (t0_value = /*episode*/
      ctx[4].episode_number + ""))
        set_data(t0, t0_value);
      if (dirty & /*episodes*/
      1 && t3_value !== (t3_value = /*episode*/
      ctx[4].title + ""))
        set_data(t3, t3_value);
      if (dirty & /*episodes*/
      1 && a_href_value !== (a_href_value = `/podcast/${podcastId}/episode/${/*episode*/
      ctx[4].episode_number}`)) {
        attr(a, "href", a_href_value);
      }
      if (dirty & /*episodes*/
      1 && t6_value !== (t6_value = /*formatDate*/
      ctx[1](
        /*episode*/
        ctx[4].publish_date
      ) + ""))
        set_data(t6, t6_value);
      if (dirty & /*episodes*/
      1 && t8_value !== (t8_value = /*episode*/
      ctx[4].transcribed ? "📃 " : "  "))
        set_data(t8, t8_value);
    },
    d(detaching) {
      if (detaching) {
        detach(li);
        detach(t9);
      }
    }
  };
}
function create_fragment$1(ctx) {
  let show_if;
  let if_block_anchor;
  function select_block_type(ctx2, dirty) {
    if (dirty & /*episodes*/
    1)
      show_if = null;
    if (show_if == null)
      show_if = !!/*episodes*/
      (ctx2[0] && Object.keys(
        /*episodes*/
        ctx2[0]
      ).length > 0);
    if (show_if)
      return create_if_block;
    return create_else_block;
  }
  let current_block_type = select_block_type(ctx, -1);
  let if_block = current_block_type(ctx);
  return {
    c() {
      if_block.c();
      if_block_anchor = empty();
    },
    l(nodes) {
      if_block.l(nodes);
      if_block_anchor = empty();
    },
    m(target, anchor) {
      if_block.m(target, anchor);
      insert_hydration(target, if_block_anchor, anchor);
    },
    p(ctx2, [dirty]) {
      if (current_block_type === (current_block_type = select_block_type(ctx2, dirty)) && if_block) {
        if_block.p(ctx2, dirty);
      } else {
        if_block.d(1);
        if_block = current_block_type(ctx2);
        if (if_block) {
          if_block.c();
          if_block.m(if_block_anchor.parentNode, if_block_anchor);
        }
      }
    },
    i: noop,
    o: noop,
    d(detaching) {
      if (detaching) {
        detach(if_block_anchor);
      }
      if_block.d(detaching);
    }
  };
}
const podcastId = "twiml-ai-podcast";
const func = (a, b) => b[0] - a[0];
function instance$1($$self, $$props, $$invalidate) {
  hooks.relativeTimeThreshold("d", 7);
  hooks.relativeTimeThreshold("w", 10);
  function formatDate(dateString) {
    const date = hooks(dateString);
    return date.format("LL");
  }
  let episodes = {};
  async function fetchEpisodes() {
    const response = await fetch(`/api/podcast/${podcastId}`);
    if (response.ok) {
      const data = await response.json();
      $$invalidate(0, episodes = data["episodes"]);
    } else {
      console.error("Error fetching episodes");
    }
  }
  {
    onMount(fetchEpisodes);
  }
  return [episodes, formatDate];
}
class Episodes extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$1, create_fragment$1, safe_not_equal, {});
  }
}
function create_fragment(ctx) {
  let div3;
  let div2;
  let div0;
  let t0_value = (
    /*podcast*/
    ctx[0].title + ""
  );
  let t0;
  let t1;
  let div1;
  let t2_value = (
    /*podcast*/
    ctx[0].description + ""
  );
  let t2;
  let t3;
  let div4;
  let episodes;
  let current;
  episodes = new Episodes({});
  return {
    c() {
      div3 = element("div");
      div2 = element("div");
      div0 = element("div");
      t0 = text(t0_value);
      t1 = space();
      div1 = element("div");
      t2 = text(t2_value);
      t3 = space();
      div4 = element("div");
      create_component(episodes.$$.fragment);
      this.h();
    },
    l(nodes) {
      div3 = claim_element(nodes, "DIV", { class: true });
      var div3_nodes = children(div3);
      div2 = claim_element(div3_nodes, "DIV", { class: true });
      var div2_nodes = children(div2);
      div0 = claim_element(div2_nodes, "DIV", { class: true });
      var div0_nodes = children(div0);
      t0 = claim_text(div0_nodes, t0_value);
      div0_nodes.forEach(detach);
      t1 = claim_space(div2_nodes);
      div1 = claim_element(div2_nodes, "DIV", { class: true });
      var div1_nodes = children(div1);
      t2 = claim_text(div1_nodes, t2_value);
      div1_nodes.forEach(detach);
      div2_nodes.forEach(detach);
      div3_nodes.forEach(detach);
      t3 = claim_space(nodes);
      div4 = claim_element(nodes, "DIV", { class: true });
      var div4_nodes = children(div4);
      claim_component(episodes.$$.fragment, div4_nodes);
      div4_nodes.forEach(detach);
      this.h();
    },
    h() {
      attr(div0, "class", "font-bold text-xl");
      attr(div1, "class", "text-gray-700 text-md py-1");
      attr(div2, "class", "px-6 py-4");
      attr(div3, "class", "mx-auto max-w-4xl py-8 rounded overflow-hidden shadow-lg");
      attr(div4, "class", "mx-auto max-w-4xl py-8");
    },
    m(target, anchor) {
      insert_hydration(target, div3, anchor);
      append_hydration(div3, div2);
      append_hydration(div2, div0);
      append_hydration(div0, t0);
      append_hydration(div2, t1);
      append_hydration(div2, div1);
      append_hydration(div1, t2);
      insert_hydration(target, t3, anchor);
      insert_hydration(target, div4, anchor);
      mount_component(episodes, div4, null);
      current = true;
    },
    p: noop,
    i(local) {
      if (current)
        return;
      transition_in(episodes.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(episodes.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      if (detaching) {
        detach(div3);
        detach(t3);
        detach(div4);
      }
      destroy_component(episodes);
    }
  };
}
function instance($$self, $$props, $$invalidate) {
  let { data } = $$props;
  const podcast = data.data;
  $$self.$$set = ($$props2) => {
    if ("data" in $$props2)
      $$invalidate(1, data = $$props2.data);
  };
  return [podcast, data];
}
class Page extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance, create_fragment, safe_not_equal, { data: 1 });
  }
}
export {
  Page as component,
  _page as universal
};
