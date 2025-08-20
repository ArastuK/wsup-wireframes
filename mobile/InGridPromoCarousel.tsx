import React, { useEffect, useMemo, useRef, useState } from "react";

export type PromoSlide = {
  id: string;
  title: string;
  description: string;
  cta?: string;
  background?: string; // css background (gradient or image url via url(...))
};

export type InGridPromoCarouselProps = {
  className?: string;
  slides?: PromoSlide[];
  heightPx?: number; // defaults to 240px to match character tiles
};

/**
 * InGridPromoCarousel
 * - Designed to be embedded inside the Explore two-column grid
 * - Spans full grid width using gridColumn: 1 / -1
 * - Horizontally scrollable with snap and pagination dots
 * - Default slides include Character Creation and Create a Taptale
 */
export const InGridPromoCarousel: React.FC<InGridPromoCarouselProps> = ({
  className,
  slides,
  heightPx = 240,
}) => {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [active, setActive] = useState(0);

  const resolvedSlides: PromoSlide[] = useMemo(
    () =>
      slides ?? [
        {
          id: "character-creation",
          title: "Character Creation",
          description: "Bring them to life",
          cta: "Learn more >",
          background:
            "linear-gradient(135deg, rgba(255,184,108,.28), rgba(124,92,255,.35)), url('https://images.unsplash.com/photo-1520975922284-8b456906c813?q=80&w=1200&auto=format&fit=crop')",
        },
        {
          id: "taptale",
          title: "Create a Taptale",
          description: "Write a story",
          cta: "Start writing >",
          background:
            "linear-gradient(135deg, rgba(123,63,228,.35), rgba(35,35,45,.65)), url('https://images.unsplash.com/photo-1520974735194-6a6d3d19b3d8?q=80&w=1200&auto=format&fit=crop')",
        },
      ],
    [slides]
  );

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const onScroll = () => {
      const width = el.clientWidth;
      const index = Math.round(el.scrollLeft / Math.max(width, 1));
      setActive(Math.min(Math.max(index, 0), resolvedSlides.length - 1));
    };
    el.addEventListener("scroll", onScroll, { passive: true });
    return () => el.removeEventListener("scroll", onScroll);
  }, [resolvedSlides.length]);

  return (
    <div
      className={"ingrid-promo-carousel" + (className ? ` ${className}` : "")}
      style={{ gridColumn: "1 / -1", height: `${heightPx}px` }}
    >
      <style>{`
        .ingrid-promo-carousel {
          position: relative;
          border-radius: 14px;
          overflow: hidden;
          background: #202024;
        }
        .ingrid-promo-carousel .slides {
          display: flex;
          overflow-x: auto;
          scroll-snap-type: x mandatory;
          scroll-behavior: smooth;
          -webkit-overflow-scrolling: touch;
          height: 100%;
        }
        .ingrid-promo-carousel .slide {
          flex: 0 0 100%;
          scroll-snap-align: start;
          position: relative;
          height: 100%;
          display: flex;
          align-items: flex-end;
          justify-content: flex-start;
          color: #fff;
          background-size: cover;
          background-position: center;
          background-repeat: no-repeat;
        }
        .ingrid-promo-carousel .slide::after {
          content: "";
          position: absolute; inset: 0;
          background: linear-gradient(180deg, rgba(0,0,0,0) 40%, rgba(0,0,0,.68) 100%);
        }
        .ingrid-promo-carousel .content {
          position: relative;
          z-index: 1;
          padding: 16px;
          width: 100%;
        }
        .ingrid-promo-carousel .eyebrow {
          display: inline-block;
          padding: 4px 10px;
          border-radius: 999px;
          font-size: 12px;
          letter-spacing: .3px;
          color: #ffd27a;
          background: rgba(255, 184, 108, 0.16);
          border: 1px solid rgba(255, 184, 108, 0.35);
          margin-bottom: 8px;
        }
        .ingrid-promo-carousel h3 {
          margin: 0 0 6px 0;
          font-size: 22px;
          line-height: 1.15;
          font-weight: 800;
          text-shadow: 0 2px 12px rgba(0,0,0,0.55);
        }
        .ingrid-promo-carousel p.desc {
          margin: 0 0 10px 0;
          font-size: 14px;
          color: #eaeaea;
          opacity: .95;
        }
        .ingrid-promo-carousel .cta {
          display: inline-flex; align-items: center; gap: 8px;
          font-size: 14px; font-weight: 600; color: #ffd27a;
        }
        .ingrid-promo-carousel .cta i { font-size: 14px; }
        .ingrid-promo-carousel .dots {
          position: absolute; left: 0; right: 0; bottom: 8px;
          display: flex; gap: 6px; justify-content: center; align-items: center;
          z-index: 2;
        }
        .ingrid-promo-carousel .dot {
          width: 6px; height: 6px; border-radius: 50%;
          background: #777; opacity: .6;
        }
        .ingrid-promo-carousel .dot.active {
          width: 16px; height: 6px; border-radius: 999px; background: #ffd27a; opacity: 1;
        }
      `}</style>

      <div ref={containerRef} className="slides" aria-label="Promotional carousel">
        {resolvedSlides.map((s) => (
          <div
            key={s.id}
            className="slide"
            style={{ background: s.background }}
            role="group"
            aria-roledescription="slide"
          >
            <div className="content">
              <span className="eyebrow">Featured</span>
              <h3>{s.title}</h3>
              <p className="desc">{s.description}</p>
              <span className="cta">
                {s.cta ?? "Learn more >"}
                <i className="fas fa-chevron-right" aria-hidden="true" />
              </span>
            </div>
          </div>
        ))}
      </div>
      <div className="dots" aria-hidden>
        {resolvedSlides.map((_, i) => (
          <span key={i} className={"dot" + (i === active ? " active" : "")} />
        ))}
      </div>
    </div>
  );
};

export default InGridPromoCarousel;


