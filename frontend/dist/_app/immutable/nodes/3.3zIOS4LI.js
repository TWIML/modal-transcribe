import { H as HttpError } from "../chunks/control.xAApMQr-.js";
import { s as safe_not_equal, n as noop } from "../chunks/scheduler.fAU1PGX9.js";
import { S as SvelteComponent, i as init, e as element, t as text, s as space, c as claim_element, b as children, f as claim_text, d as detach, h as claim_space, g as get_svelte_dataset, m as attr, a as insert_hydration, j as append_hydration, k as set_data, l as transition_in, x as group_outros, v as check_outros, n as transition_out, z as destroy_each, p as create_component, q as claim_component, r as mount_component, u as destroy_component } from "../chunks/index.yutBPzth.js";
import { e as ensure_array_like, h as hooks } from "../chunks/moment.nDPJJoOf.js";
function error(status, body) {
  throw new HttpError(status, body);
}
new TextEncoder();
async function load({ params, fetch }) {
  const { podcastId, episodeNumber } = params;
  const res = await fetch(`/api/podcast/${podcastId}/episode/${episodeNumber}`);
  if (res.status === 404) {
    error(404, {
      message: "Episode not found"
    });
  }
  const data = await res.json();
  return { data };
}
const _page = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  load
}, Symbol.toStringTag, { value: "Module" }));
function create_fragment$2(ctx) {
  let li;
  let div0;
  let p;
  let t0_value = (
    /*segment*/
    ctx[0].text + ""
  );
  let t0;
  let t1;
  let div1;
  let a0;
  let t2;
  let t3_value = formatTimestamp(
    /*segment*/
    ctx[0].start
  ) + "";
  let t3;
  let a0_href_value;
  let t4;
  let span;
  let textContent = "-";
  let t6;
  let a1;
  let t7_value = formatTimestamp(
    /*segment*/
    ctx[0].end
  ) + "";
  let t7;
  let a1_href_value;
  return {
    c() {
      li = element("li");
      div0 = element("div");
      p = element("p");
      t0 = text(t0_value);
      t1 = space();
      div1 = element("div");
      a0 = element("a");
      t2 = text("🎙 ");
      t3 = text(t3_value);
      t4 = space();
      span = element("span");
      span.textContent = textContent;
      t6 = space();
      a1 = element("a");
      t7 = text(t7_value);
      this.h();
    },
    l(nodes) {
      li = claim_element(nodes, "LI", { class: true, key: true });
      var li_nodes = children(li);
      div0 = claim_element(li_nodes, "DIV", { class: true });
      var div0_nodes = children(div0);
      p = claim_element(div0_nodes, "P", { class: true });
      var p_nodes = children(p);
      t0 = claim_text(p_nodes, t0_value);
      p_nodes.forEach(detach);
      div0_nodes.forEach(detach);
      t1 = claim_space(li_nodes);
      div1 = claim_element(li_nodes, "DIV", { class: true });
      var div1_nodes = children(div1);
      a0 = claim_element(div1_nodes, "A", {
        href: true,
        class: true,
        title: true,
        target: true,
        rel: true
      });
      var a0_nodes = children(a0);
      t2 = claim_text(a0_nodes, "🎙 ");
      t3 = claim_text(a0_nodes, t3_value);
      a0_nodes.forEach(detach);
      t4 = claim_space(div1_nodes);
      span = claim_element(div1_nodes, "SPAN", { class: true, ["data-svelte-h"]: true });
      if (get_svelte_dataset(span) !== "svelte-1br80dp")
        span.textContent = textContent;
      t6 = claim_space(div1_nodes);
      a1 = claim_element(div1_nodes, "A", {
        href: true,
        class: true,
        title: true,
        target: true,
        rel: true
      });
      var a1_nodes = children(a1);
      t7 = claim_text(a1_nodes, t7_value);
      a1_nodes.forEach(detach);
      div1_nodes.forEach(detach);
      li_nodes.forEach(detach);
      this.h();
    },
    h() {
      attr(p, "class", "text-gray-500");
      attr(div0, "class", "flex-1 min-w-0");
      attr(a0, "href", a0_href_value = `#t=${Math.floor(
        /*segment*/
        ctx[0].start
      )}`);
      attr(a0, "class", "hover:bg-gray-200 text-gray-800 py-1 px-1 rounded-l text-right");
      attr(a0, "title", "listen");
      attr(a0, "target", "_blank");
      attr(a0, "rel", "noopener noreferrer");
      attr(span, "class", "text-gray-800 py-1 px-1");
      attr(a1, "href", a1_href_value = `#t=${Math.floor(
        /*segment*/
        ctx[0].end
      )}`);
      attr(a1, "class", "hover:bg-gray-200 text-gray-800 py-1 px-1 rounded-r text-right");
      attr(a1, "title", "listen");
      attr(a1, "target", "_blank");
      attr(a1, "rel", "noopener noreferrer");
      attr(div1, "class", "sm:inline-flex sm:flex-row items-center text-xs bg-gray-100 text-gray-900 dark:text-white");
      attr(li, "class", "pb-3 sm:pb-4 py-2 border-b border-gray-200 w-full rounded-t-lg flex items-center space-x-4");
      attr(
        li,
        "key",
        /*idx*/
        ctx[1]
      );
    },
    m(target, anchor) {
      insert_hydration(target, li, anchor);
      append_hydration(li, div0);
      append_hydration(div0, p);
      append_hydration(p, t0);
      append_hydration(li, t1);
      append_hydration(li, div1);
      append_hydration(div1, a0);
      append_hydration(a0, t2);
      append_hydration(a0, t3);
      append_hydration(div1, t4);
      append_hydration(div1, span);
      append_hydration(div1, t6);
      append_hydration(div1, a1);
      append_hydration(a1, t7);
    },
    p(ctx2, [dirty]) {
      if (dirty & /*segment*/
      1 && t0_value !== (t0_value = /*segment*/
      ctx2[0].text + ""))
        set_data(t0, t0_value);
      if (dirty & /*segment*/
      1 && t3_value !== (t3_value = formatTimestamp(
        /*segment*/
        ctx2[0].start
      ) + ""))
        set_data(t3, t3_value);
      if (dirty & /*segment*/
      1 && a0_href_value !== (a0_href_value = `#t=${Math.floor(
        /*segment*/
        ctx2[0].start
      )}`)) {
        attr(a0, "href", a0_href_value);
      }
      if (dirty & /*segment*/
      1 && t7_value !== (t7_value = formatTimestamp(
        /*segment*/
        ctx2[0].end
      ) + ""))
        set_data(t7, t7_value);
      if (dirty & /*segment*/
      1 && a1_href_value !== (a1_href_value = `#t=${Math.floor(
        /*segment*/
        ctx2[0].end
      )}`)) {
        attr(a1, "href", a1_href_value);
      }
      if (dirty & /*idx*/
      2) {
        attr(
          li,
          "key",
          /*idx*/
          ctx2[1]
        );
      }
    },
    i: noop,
    o: noop,
    d(detaching) {
      if (detaching) {
        detach(li);
      }
    }
  };
}
function formatTimestamp(total_seconds) {
  let milliseconds = Math.round(total_seconds * 1e3);
  let hours = Math.floor(milliseconds / 36e5);
  milliseconds -= hours * 36e5;
  let minutes = Math.floor(milliseconds / 6e4);
  milliseconds -= minutes * 6e4;
  let seconds = Math.floor(milliseconds / 1e3);
  milliseconds -= seconds * 1e3;
  const pad = (n, d = 2) => n.toString().padStart(d, "0");
  return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}.${pad(milliseconds, 3)}`;
}
function instance$2($$self, $$props, $$invalidate) {
  let { segment } = $$props;
  let { idx } = $$props;
  $$self.$$set = ($$props2) => {
    if ("segment" in $$props2)
      $$invalidate(0, segment = $$props2.segment);
    if ("idx" in $$props2)
      $$invalidate(1, idx = $$props2.idx);
  };
  return [segment, idx];
}
class Segment extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$2, create_fragment$2, safe_not_equal, { segment: 0, idx: 1 });
  }
}
function get_each_context(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[1] = list[i];
  child_ctx[3] = i;
  return child_ctx;
}
function create_each_block(ctx) {
  let segment_1;
  let current;
  segment_1 = new Segment({
    props: {
      segment: (
        /*segment*/
        ctx[1]
      ),
      idx: (
        /*idx*/
        ctx[3]
      )
    }
  });
  return {
    c() {
      create_component(segment_1.$$.fragment);
    },
    l(nodes) {
      claim_component(segment_1.$$.fragment, nodes);
    },
    m(target, anchor) {
      mount_component(segment_1, target, anchor);
      current = true;
    },
    p(ctx2, dirty) {
      const segment_1_changes = {};
      if (dirty & /*segments*/
      1)
        segment_1_changes.segment = /*segment*/
        ctx2[1];
      segment_1.$set(segment_1_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(segment_1.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(segment_1.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(segment_1, detaching);
    }
  };
}
function create_fragment$1(ctx) {
  let ul;
  let current;
  let each_value = ensure_array_like(
    /*segments*/
    ctx[0]
  );
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block(get_each_context(ctx, each_value, i));
  }
  const out = (i) => transition_out(each_blocks[i], 1, 1, () => {
    each_blocks[i] = null;
  });
  return {
    c() {
      ul = element("ul");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      this.h();
    },
    l(nodes) {
      ul = claim_element(nodes, "UL", { class: true });
      var ul_nodes = children(ul);
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].l(ul_nodes);
      }
      ul_nodes.forEach(detach);
      this.h();
    },
    h() {
      attr(ul, "class", "transcript-list");
    },
    m(target, anchor) {
      insert_hydration(target, ul, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(ul, null);
        }
      }
      current = true;
    },
    p(ctx2, [dirty]) {
      if (dirty & /*segments*/
      1) {
        each_value = ensure_array_like(
          /*segments*/
          ctx2[0]
        );
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
            transition_in(each_blocks[i], 1);
          } else {
            each_blocks[i] = create_each_block(child_ctx);
            each_blocks[i].c();
            transition_in(each_blocks[i], 1);
            each_blocks[i].m(ul, null);
          }
        }
        group_outros();
        for (i = each_value.length; i < each_blocks.length; i += 1) {
          out(i);
        }
        check_outros();
      }
    },
    i(local) {
      if (current)
        return;
      for (let i = 0; i < each_value.length; i += 1) {
        transition_in(each_blocks[i]);
      }
      current = true;
    },
    o(local) {
      each_blocks = each_blocks.filter(Boolean);
      for (let i = 0; i < each_blocks.length; i += 1) {
        transition_out(each_blocks[i]);
      }
      current = false;
    },
    d(detaching) {
      if (detaching) {
        detach(ul);
      }
      destroy_each(each_blocks, detaching);
    }
  };
}
function instance$1($$self, $$props, $$invalidate) {
  let { segments } = $$props;
  $$self.$$set = ($$props2) => {
    if ("segments" in $$props2)
      $$invalidate(0, segments = $$props2.segments);
  };
  return [segments];
}
class Transcript extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$1, create_fragment$1, safe_not_equal, { segments: 0 });
  }
}
function create_fragment(ctx) {
  let div6;
  let div2;
  let div1;
  let div0;
  let t0_value = (
    /*episode*/
    ctx[0].title + ""
  );
  let t0;
  let t1;
  let p0;
  let t2;
  let t3_value = (
    /*episode*/
    ctx[0].episode_number + ""
  );
  let t3;
  let t4;
  let p1;
  let t5;
  let t6_value = (
    /*formatDate*/
    ctx[2](
      /*episode*/
      ctx[0].publish_date
    ) + ""
  );
  let t6;
  let t7;
  let p2;
  let t8;
  let t9_value = (
    /*episode*/
    ctx[0].html_description + ""
  );
  let t9;
  let t10;
  let a;
  let t11;
  let t12;
  let div5;
  let div4;
  let div3;
  let textContent = "Transcript";
  let t14;
  let transcript;
  let current;
  transcript = new Transcript({ props: { segments: (
    /*segments*/
    ctx[1]
  ) } });
  return {
    c() {
      div6 = element("div");
      div2 = element("div");
      div1 = element("div");
      div0 = element("div");
      t0 = text(t0_value);
      t1 = space();
      p0 = element("p");
      t2 = text("Episode Number: ");
      t3 = text(t3_value);
      t4 = space();
      p1 = element("p");
      t5 = text("Publish Date: ");
      t6 = text(t6_value);
      t7 = space();
      p2 = element("p");
      t8 = text("Description: ");
      t9 = text(t9_value);
      t10 = space();
      a = element("a");
      t11 = text("Listen to Episode");
      t12 = space();
      div5 = element("div");
      div4 = element("div");
      div3 = element("div");
      div3.textContent = textContent;
      t14 = space();
      create_component(transcript.$$.fragment);
      this.h();
    },
    l(nodes) {
      div6 = claim_element(nodes, "DIV", { class: true });
      var div6_nodes = children(div6);
      div2 = claim_element(div6_nodes, "DIV", { class: true });
      var div2_nodes = children(div2);
      div1 = claim_element(div2_nodes, "DIV", { class: true });
      var div1_nodes = children(div1);
      div0 = claim_element(div1_nodes, "DIV", { class: true });
      var div0_nodes = children(div0);
      t0 = claim_text(div0_nodes, t0_value);
      div0_nodes.forEach(detach);
      t1 = claim_space(div1_nodes);
      p0 = claim_element(div1_nodes, "P", { class: true });
      var p0_nodes = children(p0);
      t2 = claim_text(p0_nodes, "Episode Number: ");
      t3 = claim_text(p0_nodes, t3_value);
      p0_nodes.forEach(detach);
      t4 = claim_space(div1_nodes);
      p1 = claim_element(div1_nodes, "P", { class: true });
      var p1_nodes = children(p1);
      t5 = claim_text(p1_nodes, "Publish Date: ");
      t6 = claim_text(p1_nodes, t6_value);
      p1_nodes.forEach(detach);
      t7 = claim_space(div1_nodes);
      p2 = claim_element(div1_nodes, "P", { class: true });
      var p2_nodes = children(p2);
      t8 = claim_text(p2_nodes, "Description: ");
      t9 = claim_text(p2_nodes, t9_value);
      p2_nodes.forEach(detach);
      t10 = claim_space(div1_nodes);
      a = claim_element(div1_nodes, "A", { href: true, class: true });
      var a_nodes = children(a);
      t11 = claim_text(a_nodes, "Listen to Episode");
      a_nodes.forEach(detach);
      div1_nodes.forEach(detach);
      div2_nodes.forEach(detach);
      t12 = claim_space(div6_nodes);
      div5 = claim_element(div6_nodes, "DIV", { class: true });
      var div5_nodes = children(div5);
      div4 = claim_element(div5_nodes, "DIV", { class: true });
      var div4_nodes = children(div4);
      div3 = claim_element(div4_nodes, "DIV", { class: true, ["data-svelte-h"]: true });
      if (get_svelte_dataset(div3) !== "svelte-nfghbz")
        div3.textContent = textContent;
      t14 = claim_space(div4_nodes);
      claim_component(transcript.$$.fragment, div4_nodes);
      div4_nodes.forEach(detach);
      div5_nodes.forEach(detach);
      div6_nodes.forEach(detach);
      this.h();
    },
    h() {
      attr(div0, "class", "text-xl pb-3 font-medium text-black");
      attr(p0, "class", "pb-2 text-gray-500");
      attr(p1, "class", "pb-2 text-gray-500");
      attr(p2, "class", "pb-2 text-gray-500");
      attr(
        a,
        "href",
        /*episode*/
        ctx[0].episode_url
      );
      attr(a, "class", "text-blue-500");
      attr(div1, "class", "px-6 py-4");
      attr(div2, "class", "mx-auto max-w-4xl mt-4 py-8 rounded overflow-hidden shadow-lg");
      attr(div3, "class", "text-xl pb-3 font-medium text-black");
      attr(div4, "class", "px-6 py-4");
      attr(div5, "class", "mx-auto max-w-4xl mt-4 py-8 rounded overflow-hidden shadow-lg");
      attr(div6, "class", "w-full");
    },
    m(target, anchor) {
      insert_hydration(target, div6, anchor);
      append_hydration(div6, div2);
      append_hydration(div2, div1);
      append_hydration(div1, div0);
      append_hydration(div0, t0);
      append_hydration(div1, t1);
      append_hydration(div1, p0);
      append_hydration(p0, t2);
      append_hydration(p0, t3);
      append_hydration(div1, t4);
      append_hydration(div1, p1);
      append_hydration(p1, t5);
      append_hydration(p1, t6);
      append_hydration(div1, t7);
      append_hydration(div1, p2);
      append_hydration(p2, t8);
      append_hydration(p2, t9);
      append_hydration(div1, t10);
      append_hydration(div1, a);
      append_hydration(a, t11);
      append_hydration(div6, t12);
      append_hydration(div6, div5);
      append_hydration(div5, div4);
      append_hydration(div4, div3);
      append_hydration(div4, t14);
      mount_component(transcript, div4, null);
      current = true;
    },
    p: noop,
    i(local) {
      if (current)
        return;
      transition_in(transcript.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(transcript.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      if (detaching) {
        detach(div6);
      }
      destroy_component(transcript);
    }
  };
}
function instance($$self, $$props, $$invalidate) {
  let { data } = $$props;
  const episode = data.data.metadata;
  const segments = data.data.segments || [];
  hooks.relativeTimeThreshold("d", 7);
  hooks.relativeTimeThreshold("w", 10);
  function formatDate(dateString) {
    const date = hooks(dateString);
    return date.format("LL");
  }
  $$self.$$set = ($$props2) => {
    if ("data" in $$props2)
      $$invalidate(3, data = $$props2.data);
  };
  return [episode, segments, formatDate, data];
}
class Page extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance, create_fragment, safe_not_equal, { data: 3 });
  }
}
export {
  Page as component,
  _page as universal
};
