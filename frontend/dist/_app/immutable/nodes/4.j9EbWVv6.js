import { s as safe_not_equal, n as noop } from "../chunks/scheduler.fAU1PGX9.js";
import { S as SvelteComponent, i as init, e as element, c as claim_element, g as get_svelte_dataset, a as insert_hydration, d as detach } from "../chunks/index.yutBPzth.js";
function create_fragment(ctx) {
  let h1;
  let textContent = "HELLO";
  return {
    c() {
      h1 = element("h1");
      h1.textContent = textContent;
    },
    l(nodes) {
      h1 = claim_element(nodes, "H1", { ["data-svelte-h"]: true });
      if (get_svelte_dataset(h1) !== "svelte-14wdjpm")
        h1.textContent = textContent;
    },
    m(target, anchor) {
      insert_hydration(target, h1, anchor);
    },
    p: noop,
    i: noop,
    o: noop,
    d(detaching) {
      if (detaching) {
        detach(h1);
      }
    }
  };
}
class Page extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, null, create_fragment, safe_not_equal, {});
  }
}
export {
  Page as component
};
