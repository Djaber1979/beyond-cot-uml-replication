import argparse, os, yaml

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='config/config.yaml')
    args = ap.parse_args()

    # Ordered pipeline
    import src.normalize_and_dedupe as normalize
    import src.build_consensus as build
    import src.self_consistency as selfcons
    import src.post_cot_consensus as postcot
    import src.evaluate as evaluate

    normalize.run(args.config)
    build.run(args.config)
    selfcons.run(args.config)
    postcot.run(args.config)
    evaluate.run(args.config)

if __name__=='__main__':
    main()
