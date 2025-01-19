type PropsWithChildren<P> = P & JSX.ElementChildrenAttribute

type ComponentClass<P = Record<string, unknown>> = new (
  props: PropsWithChildren<P>
) => any

type FunctionComponent<P = Record<string, unknown>> = (
  props: PropsWithChildren<P>
) => any

type ComponentType<P = Record<string, unknown>> =
  | ComponentClass<P>
  | FunctionComponent<P>

// Allow one level of nesting.
export type Components = Record<
  string,
  | keyof JSX.IntrinsicElements
  | ComponentType<any>
  | Record<string, ComponentType>
> &
  Partial<{
    [TagName in keyof JSX.IntrinsicElements]:
      | keyof JSX.IntrinsicElements
      | ComponentType<JSX.IntrinsicElements[TagName]>
      // Nested components are weird for valid intrinsics, but, there are many
      // HTML element names, such as `map`, which are unlikely to be used as
      // the element, and quite likely to be used as a component map instead.
      | Record<string, ComponentType<any>>
  }>

/**
 * Props passed to the `MdxContent` component.
 * Could be anything.
 * The `components` prop is special: it defines what to use for components
 * inside the content.
 */
// type-coverage:ignore-next-line
export type MdxContentProps = {[props: string]: any; components?: Components}

/**
 * An function component which renders the MDX content using a JSX implementation.
 *
 * @param props
 *   Props passed to the `MdxContent` component.
 *   Could be anything.
 *   The `components` prop is special: it defines what to use for components
 *   inside the content.
 * @returns
 *   A JSX element.
 *   The meaning of this may depend on the project configuration.
 *   As in, it could be a React, Preact, or Vue element.
 */
export type MdxContent = (props: MdxContentProps) => JSX.Element | null

/**
 * An MDX module.
 * Exports could be anything.
 * The default export is an `MdxContent` component.
 */
export type MdxModule = {[identifier: string]: unknown; default: MdxContent}
